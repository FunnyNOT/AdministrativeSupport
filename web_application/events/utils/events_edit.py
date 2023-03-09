from datetime import datetime
import pytz

from django.contrib import messages

from events.utils.messages import ErrorMessages, SuccessMessages
from homepage.templatetags.has_group import has_group

def event_edit(request, event_obj, member_obj, logged_user_id):

    # Get request inputs
    request_id = request.POST.get('edit_event_id')
    request_title = request.POST.get('edit_event_title')
    request_description = request.POST.get('edit_event_description')
    request_datetime = request.POST.get('edit_event_datetime')
    request_visible_to_students = request.POST.get('edit_event_visible_to_students')

    request_visible_to_students = True if request_visible_to_students == 'on' else False
    
    # Get database records
    db_event = event_obj.get(id=request_id)

    # Get member record from database
    member = member_obj.get(auth_user_id=logged_user_id)

    # Check if not request datetime and put the previous one
    if not request_datetime:
        request_datetime = db_event.event_datetime

    # Check for missing information
    if not request_title or not request_description:
            # Return error message
            return messages.error(request, ErrorMessages.MISSING_INFORMATION)


    if not isinstance(request_datetime, datetime):
        # Get event datetime, convert to UTC
        request_datetime = datetime.strptime(request_datetime, '%Y-%m-%dT%H:%M')
        request_datetime = pytz.utc.localize(request_datetime)

    # Check if nothing changed
    if db_event.title == request_title and db_event.description == request_description and db_event.event_datetime == request_datetime and request_visible_to_students == db_event.visible_to_students :
        return messages.error(request, ErrorMessages.NOTHING_CHANGED)

    # Get datetime utc now
    datetime_now = datetime.utcnow().replace(tzinfo=pytz.UTC)

    # Check if the event datetime is before the current datetime
    if request_datetime <= datetime_now:
        return messages.error(request, ErrorMessages.WRONG_DATETIME)

    # Check that the new event title doesn't exist in the portal already
    if event_obj.filter(portal_id=member.portal_id, title=request_title).exclude(id=request_id).exists():
        return(messages.error(request, ErrorMessages.EVENT_TITLE_EXISTS))

                
    if has_group(request.user, ['manager']):

        # If manager belongs to the portal that tries to edit
        if member.portal_id != db_event.portal_id:
            return messages.error(request, ErrorMessages.CANNOT_EDIT_ADMIN_EVENTS)
    

    # Make the change to the database
    db_event.title = request_title
    db_event.description = request_description
    db_event.event_datetime = request_datetime
    db_event.visible_to_students = db_event.visible_to_students if request_visible_to_students == db_event.visible_to_students else not db_event.visible_to_students
    db_event.save()
    return messages.success(request, SuccessMessages.SUCCESSFUL_EDIT)