from datetime import datetime
import pytz

from django.contrib import messages
from classes.utils.messages import ErrorMessages, SuccessMessages


def class_create(request, class_obj, member_obj, logged_user_id, viewed_portal_id):

    # Get post request info
    class_name = request.POST.get('class_name')

    # Get logged user information
    member_info = member_obj.get(auth_user_id=logged_user_id)

    # Get classes based on logged user's portal
    classes = class_obj.filter(portal_id=viewed_portal_id)

    # Check class name is not empty
    if not class_name:
        return messages.error(request, ErrorMessages.EMPTY_CLASS_NAME)

    # Loop over classes
    for single_class in classes:

        # Check class_name already exists
        if single_class.name == class_name:
            return messages.error(request, ErrorMessages.CLASS_NAME_EXISTS)
  
    # Get datetime now
    datetime_now = datetime.utcnow().replace(tzinfo=pytz.UTC)

    # Create record in database
    class_obj.create(name=class_name, created_at=datetime_now, created_by_id=logged_user_id, portal_id=viewed_portal_id)
    
    # Add successful message in django messages to display
    messages.success(request, SuccessMessages.SUCCESSFUL_ENTRY)
