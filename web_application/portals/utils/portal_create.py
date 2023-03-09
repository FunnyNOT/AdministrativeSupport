from datetime import datetime
import pytz

from django.contrib import messages
from portals.utils.messages import ErrorMessages, SuccessMessage


def portal_create(request, portal_obj):


    # Get context from request 
    portal_name_1 = request.POST.get('portal_name_1')
    is_active_1 = request.POST.get('is_active_1')

    # Create a list with the portal names from context
    portal_list = [portal_name_1]
    is_active_list = [is_active_1]

    # Create a list of objects that create a record in database
    portals_list = []

    # Get datetime now
    datetime_now = datetime.utcnow().replace(tzinfo=pytz.UTC)

    # Get portal information from database
    portals_db = portal_obj.filter()

    if not portal_name_1:
        return messages.error(request, ErrorMessages.EMPTY_PORTAL_NAME)

    for counter, portal in enumerate(portal_list):

        # Check if portal name exists
        if portal:
            # Check if the name of the portal already exists
            for db_portal in portals_db:
                if db_portal.name == portal:
                    return messages.error(request, ErrorMessages.PORTAL_NAME_EXISTS)

            if is_active_list[counter] == 'on':
                is_active = 1
            else:
                is_active = 0

            
            portals_list.append({'name': portal, 'is_active': is_active, 'created_at': datetime_now})
    
    # Create a record of this portal in database
    for portal in portals_list:
        portal_obj.create(name=portal['name'], is_active=portal['is_active'], created_at=portal['created_at'])
    
    messages.success(request, SuccessMessage.SUCCESSFUL_ENTRY)
    return {'success': 1}
