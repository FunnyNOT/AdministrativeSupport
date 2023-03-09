from django.contrib import messages
from portals.utils.messages import SuccessMessage, ErrorMessages

def portal_status_change(request, portal_obj):
    
    # Get portal id from POST request
    portal_id = request.POST.get('portal_id_status')

    # Get portal record from DB
    portal_record = portal_obj.get(id=portal_id)


    # Check if the status change is for 'Admin Portal'
    if portal_record.name == 'Admin Portal':
        messages.error(request, ErrorMessages.NOT_VALID_STATUS_CHANGE)
        return {'error': 1}

    # Update the database record status
    portal_obj.filter(id=portal_id).update(is_active=not portal_record.is_active)

    # Send message success
    messages.success(request, SuccessMessage.SUCCESSFUL_STATUS_CHANGE)
    return {'success': 1}