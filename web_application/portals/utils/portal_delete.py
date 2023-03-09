from django.contrib import messages
from django.shortcuts import redirect

from portals.utils.messages import SuccessMessage

def portal_delete(request, viewed_portal_id, portal_obj, user_obj, member_obj, allow_mbr_registration_obj):
    
    # Get the portal record
    record = portal_obj.get(id=viewed_portal_id)

    # Get the members record
    members = member_obj.filter(portal_id=viewed_portal_id)

    # Get the ids of members inside the portal
    members_ids_list = members.values_list('id', flat=True) 

    # Get the auth_user records based on the list
    auth_user_in_portal = user_obj.filter(pk__in=members_ids_list)
    
    # Get records from allowed memmber_registration table that belong to the portal
    allowed_members = allow_mbr_registration_obj.filter(portal_id=viewed_portal_id)

    # -----Deletions in members, auth_user, allow_member_registration, portals------------------

    allowed_members.delete()

    auth_user_in_portal.delete()

    members.delete()    

    record.delete()

    # Add successful message
    messages.success(request, SuccessMessage.SUCCESSFUL_PORTAL_DELETE)

    return {'delete': True}