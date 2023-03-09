import pytz
from datetime import datetime

from django.contrib import messages
from members.utils.messages import ErrorMessages, SuccessMessages
from members.utils.send_email import Email
from django.conf import settings
from config import PROJECT_LINK_ORIGIN


def member_invite(request, user_obj, group_obj, portal_obj, allow_reg_obj):
    
    email = request.POST.get('invitation_email')
    portal = request.POST.get('invitation_portal')
    group = request.POST.get('invitation_group')


    # Check if something is missing
    if not email or not portal or not group:
        return messages.error(request, ErrorMessages.EMAIL_GROUP_PORTAL_FIELDS_NOT_FILLED)
    

    # Check if the email already exists
    user_emails = list(user_obj.values_list('username', flat=True))
    
    if email in user_emails:
        return messages.error(request, ErrorMessages.EMAIL_ALREADY_EXISTS)


    # Check that a system admin and admin can only be create for admin portal
    if group in ['system_admin', 'admin'] and portal!='admin_portal':
        return messages.error(request, ErrorMessages.ADMIN_WRONG_PORTAL)

    
    # Create data for email
    registration_page_link = PROJECT_LINK_ORIGIN + 'register/'
    email_sender = settings.EMAIL_HOST_USER
    subject = r'Invitation to join the bachelor thesis project platform'
    body = f'''You were invited to join the plaform as a {group} in the {portal}.\n\nPlease use the link {registration_page_link} to join. \n\nBest Regards,\nThe Bachelor Thesis Project Team'''
    
    # Create data for the record in database
    group_id = group_obj.filter(name=group)[0].id
    portal_id = portal_obj.filter(name=portal)[0].id
    
    datetime_now = datetime.utcnow().replace(tzinfo=pytz.UTC).strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        user_in_database = allow_reg_obj.filter(username=email)
        
        # If the user is already invited
        if user_in_database:
            
            # Get the invitation counter
            invitation = allow_reg_obj.filter(username=email)[0]
        
            if not invitation.is_registered:
            
                allow_reg_obj.filter(username=email).update(last_updated_date=datetime_now,
                                                            invitation_counter=invitation.invitation_counter + 1,
                                                            group_id=group_id,
                                                            portal_id=portal_id)
            else:
                # Check if the user is already registered in the platform
                return messages.error(request, ErrorMessages.USER_ALREADY_REGISTERED)

        # If the user isn't invited yet
        else:
            
            # Create a record in database allow_member_registration table
            allow_reg_obj.create(username=email,
                                is_registered=False,
                                group_id=group_id,
                                portal_id=portal_id,
                                created_date=datetime_now,
                                invitation_counter=1)


        # Create the email object
        email_obj = Email(subject = subject, body = body, email_sender = email_sender, email_attachment_data = None, email_recipient = email)
        
        # Send the email
        email_obj.send_email()

        return messages.success(request, SuccessMessages.SUCCESSFUL_INVITATION)
    
    except Exception as e:
        return messages.error(request, ErrorMessages.SOMETHING_WENT_WRONG)

