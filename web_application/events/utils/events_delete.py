from django.contrib import messages

from homepage.templatetags.has_group import has_group
from events.utils.messages import SuccessMessages, ErrorMessages

def event_delete(request, event_obj, member_obj, logged_user_id):

    # Get the announcement_id from the request
    event_id = request.POST.get('delete_event_id')

    # Get the announcement record from db
    db_event = event_obj.get(id=event_id)

    # Check if the user is admin, system_admin or manager
    if has_group(request.user, ['admin', 'system_admin']):
        
        # Delete the announcement record
        db_event.delete()

        # Return success message
        return messages.success(request, SuccessMessages.SUCCESSFUL_DELETION)

    elif has_group(request.user, ['manager']):
        
        # Get member record from db
        member = member_obj.get(id=logged_user_id)

        # If manager belongs to the portal that tries to delete
        if member.portal_id == db_event.portal_id:
            
            # Delete the record from db
            db_event.delete()

            # Return success message
            return messages.success(request, SuccessMessages.SUCCESSFUL_DELETION)
        else:

            # Return error message
            return messages.error(request, ErrorMessages.CANNOT_DELETE_ADMIN_EVENTS)
