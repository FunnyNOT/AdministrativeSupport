from django.shortcuts import render, redirect

from members.utils.basic_context import get_basic_context
from members.utils.member_invitation import member_invite
from members.utils.member_view_list import invitation_modal, members_view_list
from members.utils.csv_export_members import csv_export_members
from members.utils.member_profile import member_profile_view
from members.utils.member_profile_edit import member_profile_edit
from classes.models import Class, Student
from portals.models import Portal

from django.contrib.auth.models import Group, User
from members.models import AllowMemberRegistration, Member

# Get all objects from database
group_obj = Group.objects
user_obj = User.objects
portal_obj = Portal.objects
member_obj = Member.objects
class_obj = Class.objects
student_obj = Student.objects
allow_reg_obj = AllowMemberRegistration.objects


def members_view(request):

    # Get logged_user_id
    logged_user_id = request.user.id
    
    # Get context basic
    context_b = get_basic_context(logged_user_id, search_bar=True)

    # Get context for the invitation modal
    context_invitation_modal = invitation_modal(request, portal_obj, group_obj, user_obj)

    context_view_list = members_view_list(request, member_obj)

    if request.method == 'GET':
        
        # Merge the context
        context = {'context_basic': context_b, 'context_view_list': context_view_list, 'context_invitation_modal': context_invitation_modal}

        return render(request, 'members.html', context)

    
    if request.method == 'POST':
        
        # Get the action from the POST request
        members_action = request.POST.get('members_action')

        operation_dict = {
                "invite_user": lambda: member_invite(request, user_obj, group_obj, portal_obj, allow_reg_obj),
                "csv_export": lambda: csv_export_members(request),
            }

        context_operational = operation_dict.get(members_action)()

        if context_operational is None:
            return redirect('Users')
        else:
            return context_operational


def profile_view(request, viewed_user_id):

    # Get logged_user_id
    logged_user_id = request.user.id
    
    # Get context basic
    context_b = get_basic_context(logged_user_id)

    context_profile = member_profile_view(request, member_obj, user_obj, group_obj, portal_obj, class_obj, student_obj, viewed_user_id, logged_user_id)
    

    if request.method == 'GET':
        
        # Merge the context
        context = {'context_basic': context_b, 'context_profile': context_profile}

        return render(request, 'member_profile.html', context)


    if request.method == 'POST':

        # Get the action from the POST request
        member_profile_action = request.POST.get('member_profile_action')

        operation_dict = {
                "edit_profile": lambda: member_profile_edit(request, user_obj, group_obj, portal_obj, allow_reg_obj, member_obj, student_obj, viewed_user_id)
            }

        context_operational = operation_dict.get(member_profile_action)()

        return redirect('Profile' , viewed_user_id)
        