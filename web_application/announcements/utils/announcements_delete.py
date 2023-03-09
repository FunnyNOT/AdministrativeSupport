from django.contrib import messages

from homepage.templatetags.has_group import has_group
from announcements.utils.messages import SuccessMessage, ErrorMessages

def announcement_delete(request, announcements_obj, member_obj, logged_user_id):

    # Get the announcement_id from the request
    announcement_id = request.POST.get('delete_announcement_id')

    # Get the announcement record from db
    this_announcement = announcements_obj.get(id=announcement_id)

    # Check if the user is admin, system_admin or manager
    if has_group(request.user, ['admin', 'system_admin']):
        
        # Delete the announcement record
        this_announcement.delete()

        # Return success message
        return messages.success(request, SuccessMessage.SUCCESSFUL_DELETION)

    elif has_group(request.user, ['manager']):
        
        # Get member record from db
        member = member_obj.get(id=logged_user_id)

        # If manager belongs to the portal that tries to delete
        if member.portal_id == this_announcement.portal_id:
            
            # Delete the record from db
            this_announcement.delete()

            # Return success message
            return messages.success(request, SuccessMessage.SUCCESSFUL_DELETION)
        else:

            # Return error message
            return messages.error(request, ErrorMessages.CANNOT_DELETE_ADMIN_ANNOUNCEMENTS)




