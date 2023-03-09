import pytz
from datetime import datetime

from django.contrib import messages
from django.db import transaction
from members.utils.messages import ErrorMessages, SuccessMessages
from django.conf import settings
from config import PROJECT_LINK_ORIGIN

from homepage.templatetags.has_group import has_group

def member_profile_edit(request, user_obj, group_obj, portal_obj, allow_reg_obj, member_obj, student_obj, viewed_user_id):

    new_first_name = request.POST.get('edit_first_name')
    new_last_name = request.POST.get('edit_last_name')

    # Get record for this user from database
    this_user = user_obj.get(id=viewed_user_id)

    # Check first name or last name being empty
    if not new_first_name or not new_last_name:
        return messages.error(request, ErrorMessages.MISSING_INFORMATION)

    # Check nothing changed
    if this_user.first_name == new_first_name and this_user.last_name == new_last_name:
        return messages.error(request, ErrorMessages.NOTHING_CHANGED)

    

    with transaction.atomic():
        # Change first name last name of auth user table
        this_user = user_obj.get(id=viewed_user_id)
        this_user.first_name=new_first_name
        this_user.last_name=new_last_name


        # Change first name last name of member table
        this_member = member_obj.get(auth_user_id=viewed_user_id)
        this_member.first_name = new_first_name
        this_member.last_name = new_last_name

        # Check if the user is student
        if has_group(request.user, ['student']):

            # Change first name, last name of student table
            this_student = student_obj.get(auth_user_id=viewed_user_id)
            this_student.first_name = new_first_name
            this_student.last_name = new_last_name

            this_student.save()
            


        this_user.save()
        this_member.save()
        return messages.success(request, SuccessMessages.SUCCESSFUL_EDIT)
