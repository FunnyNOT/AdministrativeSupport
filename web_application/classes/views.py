from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User, Group

from members.utils.basic_context import get_basic_context
from members.models import Member, AllowMemberRegistration
from classes.utils import class_list, class_create, class_profile, class_edit, student_create, student_edit, student_delete, assigned_teacher_edit, file_upload, timetable
from classes.models import Class, Student, StudentGrade
from portals.models import Portal


class_obj = Class.objects
member_obj = Member.objects
student_obj = Student.objects
student_grade_obj = StudentGrade.objects
portal_obj = Portal.objects
user_obj = User.objects
group_obj = Group.objects
allow_mbr_registration_obj = AllowMemberRegistration.objects

@permission_required("classes.can_view_class")
def classes_view(request, viewed_portal_id):

    logged_user_id = request.user.id

    if request.method == 'GET':

        # Get context basic
        context_b = get_basic_context(logged_user_id)

        context_classes = class_list.class_view_list(request, user_obj, class_obj, member_obj, student_obj, logged_user_id, viewed_portal_id)

        context = {'context_basic': context_b, 'context_classes': context_classes}

        return render(request, 'classes_list.html', context)
    
    elif request.method == 'POST':

        # Get the action from the POST request
        classes_action = request.POST.get('classes_action')
        
        operation_dict = {
                "create_class": lambda: class_create.class_create(request, class_obj, member_obj, logged_user_id, viewed_portal_id),
            }

        context_operational = operation_dict.get(classes_action)()
        
        # If the viewed portal is deleted redirect to Portals list page instead
        return redirect('Classes', viewed_portal_id=str(viewed_portal_id))
        

def class_profile_view(request, viewed_portal_id, viewed_class_id, **kwargs):    

    logged_user_id = request.user.id

    if request.method == 'GET':

        # Get context basic
        context_b = get_basic_context(logged_user_id)

        context_class_profile = class_profile.class_profile_view(request, user_obj, group_obj, class_obj, member_obj, student_obj, student_grade_obj, logged_user_id, viewed_portal_id, viewed_class_id)

        context = {'context_basic': context_b, 'context_class_profile': context_class_profile}

        return render(request, 'classes_profile.html', context)

    elif request.method == 'POST':
        # Get the action from the POST request
        class_profile_action = request.POST.get('class_profile_action')

        operation_dict = {
            "edit_class": lambda: class_edit.class_edit(request, class_obj, member_obj, viewed_portal_id, viewed_class_id, logged_user_id),
            "add_student": lambda: student_create.student_create(request, user_obj, class_obj, member_obj, allow_mbr_registration_obj, student_obj, student_grade_obj, portal_obj, viewed_portal_id, viewed_class_id, logged_user_id),
            "edit_student": lambda: student_edit.student_edit(request, user_obj, class_obj, member_obj, student_obj, student_grade_obj, viewed_portal_id, viewed_class_id, logged_user_id),
            "delete_student": lambda: student_delete.student_delete(request, user_obj, allow_mbr_registration_obj, class_obj, member_obj, student_obj, student_grade_obj, viewed_portal_id, viewed_class_id, logged_user_id),
            "edit_assigned_teacher": lambda: assigned_teacher_edit.assigned_teacher_edit(request, class_obj, member_obj, student_obj, student_grade_obj, viewed_portal_id, viewed_class_id, logged_user_id)
            }

        context_operational = operation_dict.get(class_profile_action)()
        

        # If the viewed portal is deleted redirect to Portals list page instead
        return redirect('Class Profile', viewed_portal_id=str(viewed_portal_id), viewed_class_id=str(viewed_class_id))


def class_timetable_view(request, viewed_portal_id, viewed_class_id):

    logged_user_id = request.user.id

    if request.method == 'GET':
        # Get context basic
        context_b = get_basic_context(logged_user_id)

        context_timetable = timetable.timetable_view(request, viewed_portal_id, viewed_class_id)

        context = {'context_basic': context_b, 'context_timetable': context_timetable}

        return render(request, 'classes_timetable.html', context)

    elif request.method == 'POST':

        # Get the action from the POST request
        class_timetable_action = request.POST.get('timetable_action')

        operation_dict = {
            "file_upload": lambda: file_upload.file_upload(request, class_obj, member_obj, viewed_portal_id, viewed_class_id, logged_user_id),
            }

        context_operational = operation_dict.get(class_timetable_action)()
        

        # If the viewed portal is deleted redirect to Portals list page instead
        return redirect('Class Timetable', viewed_portal_id=str(viewed_portal_id), viewed_class_id=str(viewed_class_id))




