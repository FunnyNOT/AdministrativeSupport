from datetime import datetime
import pytz

from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate

from account.utils.messages import LoginMessages
from members.utils.event_types import EventTypes


def login_view(request, user_obj, analytics_members_obj, member_obj, portal_obj):
    

    # Authenticate user 
    username = request.POST['user_email']
    password = request.POST['user_password']

    user = authenticate(username=username, password=password)

    # check if wrong credentials
    wrong_credentials = False
    try:
        auth_user = user_obj.filter(username=username)[0]
        wrong_credentials = True
    except:
        pass

    # Check if user exists
    if user is not None:
        auth_user = user_obj.filter(username=username)[0]

        member_record = member_obj.get(auth_user_id=user.id)

        user_portal = portal_obj.get(id=member_record.portal_id)

        if user_portal.is_active == 0:
            return messages.error(request, LoginMessages.PORTAL_INACTIVE)

        # Check if account is inactive
        if not auth_user.is_active:
            return messages.error(request, LoginMessages.ACCOUNT_INACTIVE)

        login(request, user)

        datetime_now = datetime.utcnow().replace(tzinfo=pytz.UTC)

        session_hash_number = request.session.get('session_hash_number')

        analytics_members_obj.create(timestamp=datetime_now,
                                     event_type=EventTypes.LOGIN,
                                     session_hash_number=session_hash_number,
                                     auth_user_id=user.id,
                                     portal_id=member_record.portal_id)

        return {'success': 1}
    else:
        if wrong_credentials:
            return messages.error(request, LoginMessages.WRONG_CREDENTIALS)
        else:
            return messages.error(request, LoginMessages.INEXISTANT_ACCOUNT)

    