from datetime import datetime
import pytz

from django.contrib import messages

from announcements.utils.messages import ErrorMessages, SuccessMessage

def announcement_create(request, announcements_obj, member_obj, logged_user_id):


    new_title = request.POST.get('create_announcement_title')
    new_body = request.POST.get('create_announcement_body')
    new_visible_to_students = request.POST.get('visible_to_students')

    
    if not new_title or not new_body:
        # Return error message
        return messages.error(request, ErrorMessages.MISSING_INFORMATION)

    # Get member record from database
    member = member_obj.get(auth_user_id=logged_user_id)
    
    # Get the records of announcements for the portal that the creator belongs
    announcements = announcements_obj.filter(portal_id=member.portal_id)

    datetime_now = datetime.utcnow().replace(tzinfo=pytz.UTC)

    # Loop over the announcements and check if title already exists
    for announcement in announcements:

        # If title already exists for this portal
        if new_title == announcement.title:
            # Return error message
            return messages.error(request, ErrorMessages.ANNOUNCEMENT_TITLE_EXISTS)

    # Create the record in the database
    announcements_obj.create(title=new_title, 
                             body=new_body,
                             is_active=True,
                             visible_to_students=True if new_visible_to_students == 'on' else False, 
                             created_at=datetime_now, 
                             created_by_id=logged_user_id, 
                             portal_id=member.portal_id)

    # Return successful message
    return messages.success(request, SuccessMessage.SUCCESSFUL_CREATION)
