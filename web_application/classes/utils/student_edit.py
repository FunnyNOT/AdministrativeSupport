from datetime import datetime
from msilib.schema import Error
import pytz

from django.contrib import messages
from django.db import transaction
from classes.utils.messages import ErrorMessages, SuccessMessages




def student_edit(request, user_obj, class_obj, member_obj, student_obj, student_grade_obj, viewed_portal_id, viewed_class_id, logged_user_id):

    # Get the request.POST values
    student_choice = request.POST.get('student_choice')
    new_first_name = request.POST.get('edit_student_first_name')
    new_last_name = request.POST.get('edit_student_last_name')
    new_absences = request.POST.get('edit_student_absences')
    new_maths = request.POST.get('edit_student_maths')
    new_physics = request.POST.get('edit_student_physics')
    new_chemistry = request.POST.get('edit_student_chemistry')
    new_english = request.POST.get('edit_student_english')
    new_geography = request.POST.get('edit_student_geography')
    new_history = request.POST.get('edit_student_history')
    new_biology = request.POST.get('edit_student_biology')

    if student_choice is None:
        return messages.error(request, ErrorMessages.SELECT_STUDENT)

    # Get student record and student_grade record from database
    this_student = student_obj.get(email=student_choice)
    this_student_grades = eval(student_grade_obj.get(student_id=this_student.id).grades)

    auth_user_student = user_obj.get(username=this_student.email)

    if not new_first_name:
        new_first_name = auth_user_student.first_name
    if not new_last_name:
        new_last_name = auth_user_student.last_name
    if not new_absences:
        new_absences = this_student.absences

    # Check if marks for subjects have changed or not
    if not new_maths and not new_physics and not new_chemistry and not new_english and not new_geography and not new_history and not new_biology:
        flag_subject_changed = False
    else:
        flag_subject_changed = True

    if not new_maths:
        new_maths = this_student_grades['maths']
    if not new_physics:
        new_physics = this_student_grades['physics']
    if not new_chemistry:
        new_chemistry = this_student_grades['chemistry']
    if not new_english:
        new_english = this_student_grades['english']
    if not new_geography:
        new_geography = this_student_grades['geography']
    if not new_history:
        new_history = this_student_grades['history']
    if not new_biology:
        new_biology = this_student_grades['biology']
        
        
    # Check nothing changed
    if new_first_name == auth_user_student.first_name and new_last_name == auth_user_student.last_name and new_absences == this_student.absences and new_maths == this_student_grades['maths'] and new_physics == this_student_grades['physics'] and new_chemistry == this_student_grades['chemistry'] and new_english == this_student_grades['english'] and new_geography == this_student_grades['geography'] and new_history == this_student_grades['history'] and new_biology == this_student_grades['biology']:
        return messages.error(request, ErrorMessages.NOTHING_CHANGED)

    if flag_subject_changed:

        grades_dictionary  = {'maths': new_maths,
                            'physics': new_physics,
                            'chemistry': new_chemistry,
                            'english': new_english,
                            'geography': new_geography,
                            'history': new_history,
                            'biology': new_biology}

        new_average = (float(new_maths) + float(new_physics) + float(new_chemistry) + float(new_english) + float(new_geography) + float(new_history) + float(new_biology)) / 7

    try:
        with transaction.atomic():
            
            # Update auth_user record
            user_obj.filter(username=this_student.email).update(first_name=new_first_name,
                                                                         last_name=new_last_name)
            # Update student record
            student_obj.filter(id=this_student.id).update(absences=new_absences)

            # Update student grades record
            if flag_subject_changed:
                student_grade_obj.filter(id=this_student.id).update(grades=grades_dictionary,
                                                                    average_grade=new_average)
        # Return success msg
        return messages.success(request, SuccessMessages.SUCCESSFUL_STUDENT_EDIT)
    except Exception as e:
        print(e)
        return messages.error(request, ErrorMessages.SOMETHING_WENT_WRONG)


