import re
from datetime import datetime
import pytz

from django.db import transaction
from django.contrib import messages
from django.contrib.auth.hashers import make_password


from members.models import AllowMemberRegistration
from account.utils.messages import RegistrationMessages, GenericMessages


def register_view(request, user_obj, member_obj, portal_obj, user_groups_obj):

     # Get all the context from post
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    repeat_password = request.POST.get('repeat_password')

    # Check first name is none
    if not first_name:
        return messages.error(request, RegistrationMessages.EMPTY_FIRST_NAME)

    # Check last name is none
    if not last_name:
        return messages.error(request, RegistrationMessages.EMPTY_LAST_NAME)
    
    # Check email is none
    if not email:
        return messages.error(request, RegistrationMessages.EMPTY_EMAIL)

    # Check password is none
    if not password:
        return messages.error(request, RegistrationMessages.EMPTY_PASSWORD)

    # Check repeat password is none
    if not repeat_password:
        return messages.error(request, RegistrationMessages.EMPTY_PASSWORD)


    # Regex check valid email
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.fullmatch(regex, email):
        return messages.error(request, RegistrationMessages.NOT_VALID_EMAIL)

    # Check email is allowed to register
    allowed_emails = AllowMemberRegistration.objects.filter(username=email)

    if not allowed_emails:
        return messages.error(request, RegistrationMessages.EMAIL_NOT_INVITED)

    elif allowed_emails[0].is_registered == 1:
        return messages.error(request, RegistrationMessages.EMAIL_ALREADY_REGISTERED)

    # Check password applies to regex and repeat password is the same as password
    ''' regex = r'[A-Za-z0-9@#$%^&+=]{8,}'
    if not re.fullmatch(regex, password):
        return messages.error(request, RegistrationMessages.NOT_VALID_PASSWORD)'''

    if password != repeat_password:
        return messages.error(request, RegistrationMessages.PASSWORDS_DONT_MATCH)

    try:
        with transaction.atomic():

            # Create record in Users with the information from register
            encrypted_password = make_password(password)
            datetime_now = datetime.utcnow().replace(tzinfo=pytz.UTC)

            # Create record in default User django table
            user_obj.create(first_name=first_name,
                            last_name=last_name,
                            username=email,
                            password=encrypted_password,
                            date_joined=datetime_now)
            
            # Get the record created in database
            db_user = user_obj.filter(username=email)[0]

            # Create a record to assign this user to a group
            invitation_group = user_groups_obj.get(id=allowed_emails[0].group_id)
            invitation_group.user_set.add(db_user)
            
            # Create record in members table
            member_obj.create(is_registered=True,
                              created_at=datetime_now,
                              auth_user_id=db_user.id,
                              group_id=allowed_emails[0].group_id,
                              portal_id=allowed_emails[0].portal_id)
            

            # Add user to the portal database table for the successful registration
            portal = portal_obj.get(id=allowed_emails[0].portal_id)
            portal.users = portal.users + 1
            portal.save()

            AllowMemberRegistration.objects.filter(username=db_user.username).update(is_registered=True)
            
            return {'success': 1}
    except Exception as e:
        print(e)
        return messages.error(request, GenericMessages.SOMETHING_WENT_WRONG)
