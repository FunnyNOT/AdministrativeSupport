from django.contrib import messages
from classes.utils.messages import ErrorMessages, SuccessMessages


def class_edit(request, class_obj, member_obj, viewed_portal_id, viewed_class_id, logged_user_id):

    # Get new class name
    new_class_name = request.POST.get('edit_class_name')

    # Get this class from database

    this_class = class_obj.get(id=viewed_class_id)

    # Get the record from database
    all_portal_classes = class_obj.filter(portal_id=viewed_portal_id)
    
    # Check if nothing changed
    if new_class_name == this_class.name:
        return messages.error(request, ErrorMessages.NOTHING_CHANGED)
    
    # Check if class_name is empty
    if not new_class_name:
        return messages.error(request, ErrorMessages.EMPTY_CLASS_NAME)

    # Check if class name already exists
    for portal_class in all_portal_classes:
        if portal_class.name == new_class_name:
            return messages.error(request, ErrorMessages.CLASS_NAME_EXISTS)
    
    this_class.name = new_class_name
    this_class.save()

    return messages.success(request, SuccessMessages.SUCCESSFUL_CLASS_EDIT)

