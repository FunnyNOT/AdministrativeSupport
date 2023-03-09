from datetime import datetime
import pytz

from django.contrib import messages

from events.utils.messages import ErrorMessages, SuccessMessages

def event_create(request, event_obj, member_obj, logged_user_id):

    new_title = request.POST.get('create_event_title')
    new_description = request.POST.get('create_event_description')
    new_event_datetime = request.POST.get('create_event_datetime')
    new_event_visible_to_students = request.POST.get('visible_to_students')

    if not new_title or not new_description or not new_event_datetime:
        # Return error message
        return messages.error(request, ErrorMessages.MISSING_INFORMATION)

    # Get datetime utc now
    datetime_now = datetime.utcnow().replace(tzinfo=pytz.UTC)

    # Get event datetime, convert to UTC
    new_datetime_format = datetime.strptime(new_event_datetime, '%Y-%m-%dT%H:%M')
    new_datetime_format = pytz.utc.localize(new_datetime_format)

    # Check if the event datetime is before the current datetime
    if new_datetime_format <= datetime_now:
        return messages.error(request, ErrorMessages.WRONG_DATETIME)

    # Get member record from database
    member = member_obj.get(auth_user_id=logged_user_id)
    
    # Get the records of events for the portal that the creator belongs
    events = event_obj.filter(portal_id=member.portal_id)

    # Loop over the events and check if title already exists
    for event in events:

        # If title already exists for this portal
        if new_title == event.title:
            # Return error message
            return messages.error(request, ErrorMessages.EVENT_TITLE_EXISTS)

    # Create the record in the database
    event_obj.create(title=new_title, 
                    description=new_description, 
                    event_datetime=new_datetime_format, 
                    is_active=True, 
                    visible_to_students=True if new_event_visible_to_students == 'on' else False, 
                    created_at=datetime_now, 
                    created_by_id=logged_user_id, 
                    portal_id=member.portal_id)

    # Return successful message
    return messages.success(request, SuccessMessages.SUCCESSFUL_CREATION)