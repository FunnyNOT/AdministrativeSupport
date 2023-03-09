from datetime import datetime
from msilib.schema import Error
import pytz

from django.contrib import messages
from django.db import transaction
from classes.utils.messages import ErrorMessages, SuccessMessages



def student_delete(request, user_obj, allow_mbr_registration_obj, class_obj, member_obj, student_obj, student_grade_obj, viewed_portal_id, viewed_class_id, logged_user_id):

    # Get student choice to delete
    student_choice = request.POST.get('delete_student_choice')
    
    # Check if student choice is None
    if student_choice is None:
        return messages.error(request, ErrorMessages.SELECT_STUDENT)

    # Get the student record from database
    this_student = student_obj.get(email=student_choice)

    # Get auth_user this student
    auth_user_this_student = user_obj.get(username=this_student.email)
    
    try:
        with transaction.atomic():

            # Delete the student grades and the student from database tables
            student_obj.filter(id=this_student.id).delete()

            # Delete the student from auth_user
            user_obj.filter(username=this_student.email).delete()

            # Delete the stundet from allow_member_registration
            allow_mbr_registration_obj.filter(username=this_student.email).delete()


            return messages.success(request, SuccessMessages.SUCCESSFUL_STUDENT_DELETE)
    
    except Exception as e:
        print(e)
        return messages.error(request, ErrorMessages.SOMETHING_WENT_WRONG)
