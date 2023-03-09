from django.contrib import messages
from portals.utils.messages import ErrorMessages, SuccessMessage


def portal_edit(request, viewed_portal_id, portal_obj):


    new_portal_name = request.POST.get('portal_name')

    # Get the record from database with the portal id
    portal = portal_obj.filter(id=viewed_portal_id)[0]

    # Get portal information from database
    portals_db = portal_obj.filter()

    if portal.name == new_portal_name:
        return messages.error(request, ErrorMessages.NOTHING_CHANGED)

    # Check if the name of the portal already exists
    for db_portal in portals_db:
        if db_portal.name == new_portal_name:
            return messages.error(request, ErrorMessages.PORTAL_NAME_EXISTS)

    # Check if new_portal_name is empty
    if not new_portal_name:
        return messages.error(request, ErrorMessages.EMPTY_PORTAL_NAME)

    # Successful edit of portal
    portal.name = new_portal_name
    portal.save()
    return messages.success(request, SuccessMessage.SUCCESSFUL_PORTAL_EDIT)

    