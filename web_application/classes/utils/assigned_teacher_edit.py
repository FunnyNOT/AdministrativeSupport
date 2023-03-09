from datetime import datetime
from email import message
import pytz

from django.contrib import messages
from classes.utils.messages import ErrorMessages, SuccessMessages


def assigned_teacher_edit(request, class_obj, member_obj, student_obj, student_grade_obj, viewed_portal_id, viewed_class_id, logged_user_id):

    # Get the id of the new assigned teacher for this class
    new_assigned_teacher_id = request.POST.get('edit_assigned_teacher_choice')


    # If the id is empty
    if not new_assigned_teacher_id:
        return messages.error(request, ErrorMessages.SELECT_TEACHER)

    # Get this class record from database
    this_class = class_obj.get(id=viewed_class_id)
    
    # Check if the new teacher is the same with the one in db
    if new_assigned_teacher_id == str(this_class.assigned_teacher_id):
        return messages.error(request, ErrorMessages.TEACHER_SELECTED_IS_THE_SAME)

    
    # Get this class teachers
    possible_assigned_teachers = member_obj.filter(portal_id=viewed_portal_id, group_id=4).values_list('id', flat=True)

    # Check if the new teacher belongs this portal
    if int(new_assigned_teacher_id) not in possible_assigned_teachers:
        return messages.error(request, ErrorMessages.TEACHER_DOESNT_BELONG_TO_PORTAL)
    

    # Make the appropriate changes in the database and return success message
    this_class.assigned_teacher_id = int(new_assigned_teacher_id)
    this_class.save()

    return messages.success(request, SuccessMessages.SUCCESSFUL_ASSIGNED_TEACHER_EDIT)






