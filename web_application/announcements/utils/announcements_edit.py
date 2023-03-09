from django.contrib import messages

from homepage.templatetags.has_group import has_group
from announcements.utils.messages import SuccessMessage, ErrorMessages


def announcement_edit(request, announcements_obj, member_obj, logged_user_id):

    # Get request inputs
    request_id = request.POST.get('edit_announcement_id')
    request_title = request.POST.get('edit_announcement_title')
    request_body = request.POST.get('edit_announcement_body')
    request_visible_to_students = request.POST.get('edit_announcement_visible_to_students')
    
    request_visible_to_students = True if request_visible_to_students == 'on' else False

    # Get database records
    db_announcement = announcements_obj.get(id=request_id)

    # Get member record from database
    member = member_obj.get(auth_user_id=logged_user_id)

    # Check for missing information
    if not request_title or not request_body:
        # Return error message
        return messages.error(request, ErrorMessages.MISSING_INFORMATION)

    # Check if nothing changed
    if db_announcement.title == request_title and db_announcement.body == request_body and request_visible_to_students == db_announcement.visible_to_students:
        return messages.error(request, ErrorMessages.NOTHING_CHANGED)

    # Check that the new announcement title doesn't exist in the portal already
    if announcements_obj.filter(portal_id=member.portal_id, title=request_title).exclude(id=request_id).exists():
        return(messages.error(request, ErrorMessages.ANNOUNCEMENT_TITLE_EXISTS))

                
    if has_group(request.user, ['manager']):

        # If manager belongs to the portal that tries to edit
        if member.portal_id != db_announcement.portal_id:
            return messages.error(request, ErrorMessages.CANNOT_EDIT_ADMIN_ANNOUNCEMENTS)
    

    # Make the change to the database
    db_announcement.title = request_title
    db_announcement.body = request_body
    db_announcement.visible_to_students = db_announcement.visible_to_students if request_visible_to_students == db_announcement.visible_to_students else not db_announcement.visible_to_students
    db_announcement.save()
    return messages.success(request, SuccessMessage.SUCCESSFUL_EDIT)