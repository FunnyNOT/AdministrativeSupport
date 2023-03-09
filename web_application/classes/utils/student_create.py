from datetime import datetime
from re import A
from tkinter import E
import pytz

from django.contrib import messages
from django.db import transaction
from classes.utils.messages import ErrorMessages, SuccessMessages
from members.utils.send_email import Email
from email_configuration import EmailConfiguration
from config import PROJECT_LINK_ORIGIN


def student_create(request, user_obj, class_obj, member_obj, allow_mbr_registration_obj, student_obj, student_grade_obj, portal_obj, viewed_portal_id, viewed_class_id, logged_user_id):

    # Get the request.POST values
    first_name = request.POST.get('add_student_first_name')
    last_name = request.POST.get('add_student_last_name')
    email = request.POST.get('add_student_email')
    absences = request.POST.get('add_student_absences')
    maths = request.POST.get('add_student_maths')
    physics = request.POST.get('add_student_physics')
    chemistry = request.POST.get('add_student_chemistry')
    english = request.POST.get('add_student_english')
    geography = request.POST.get('add_student_geography')
    history = request.POST.get('add_student_history')
    biology = request.POST.get('add_student_biology')

    
    if not first_name or not last_name or not email:
        return messages.error(request, ErrorMessages.PERSONAL_FIELD_EMPTY)

    if not maths or not physics or not chemistry or not english or not geography or not history or not biology:
        return messages.error(request, ErrorMessages.MARK_FIELD_EMPTY)
        
    
    # Put 0 absences when None is given
    if not absences:
        absences = 0


    average = (float(maths) + float(physics) + float(chemistry) + float(english) + float(geography) + float(history) + float(biology)) / 7


    grades_dictionary  = {'maths': maths,
                         'physics': physics,
                         'chemistry': chemistry,
                         'english': english,
                         'geography': geography,
                         'history': history,
                         'biology': biology}
    
    # Get allow_member_registation record with the same email
    allow_registration_record = allow_mbr_registration_obj.filter(username=email)

    if not allow_registration_record:
    
        try:
            with transaction.atomic():

                # Get datetime now
                datetime_now = datetime.utcnow().replace(tzinfo=pytz.UTC)

                # Create a student record
                student_obj.create( email=email,
                                    belongs_to_class=1,
                                    absences=absences,
                                    class_id_id=viewed_class_id)

                # Get the record of the student created
                this_student = student_obj.get(email=email)
                
                # Create a student grade record
                student_grade_obj.create(grades=str(grades_dictionary),
                                        average_grade=average,
                                        student_id = this_student.id)
                
                # Create an allow_member_registration record in database
                allow_mbr_registration_obj.create(username=email,
                                                    is_registered=0,
                                                    created_date=datetime_now,
                                                    last_updated_date=datetime_now,
                                                    invitation_counter=1,
                                                    group_id=5,
                                                    portal_id=viewed_portal_id)
                
                # Get viewed portal id record from DB
                this_portal = portal_obj.get(id=viewed_portal_id)
                
                # Create data for email
                email_sender = EmailConfiguration.USERNAME
                registration_page_link = PROJECT_LINK_ORIGIN + 'register/'
                subject = r'Invitation to join the bachelor thesis project platform'
                body = f'''You were invited to join the plaform as a student in the {this_portal.name}.\n\nPlease use the link {registration_page_link} to join. \n\nBest Regards,\nThe Bachelor Thesis Project Team'''
                
                email_object = Email(subject=subject,
                                        body=body,
                                        email_sender=email_sender,
                                        email_recipient = email)
                
                email_object.send_email()


            return messages.success(request, SuccessMessages.SUCCESSFUL_STUDENT_ADDITION)
        except Exception as e:
            print(e)

            return messages.error(request, ErrorMessages.SOMETHING_WENT_WRONG)
        
    else:

        if not allow_registration_record[0].is_registered and allow_registration_record[0].portal_id == int(viewed_portal_id): 
            #try:
            with transaction.atomic():

                allow_registration_record[0].invitation_counter = allow_registration_record[0].invitation_counter + 1

                # Get viewed portal id record from DB
                this_portal = portal_obj.get(id=viewed_portal_id)

                # Create data for email
                email_sender = EmailConfiguration.USERNAME
                registration_page_link = PROJECT_LINK_ORIGIN + 'register/'
                subject = r'Invitation to join the bachelor thesis project platform'
                body = f'''You were invited to join the plaform as a student in the {this_portal.name}.\n\nPlease use the link {registration_page_link} to join. \n\nBest Regards,\nThe Bachelor Thesis Project Team'''
                
                email_object = Email(subject=subject,
                                    body=body,
                                    email_sender=email_sender,
                                    email_recipient = email)
                
                email_object.send_email()

                return messages.success(request, SuccessMessages.SUCCESSFUL_STUDENT_INVITATION)

            '''except Exception as e:
                print(e)
                return messages.error(request, ErrorMessages.SOMETHING_WENT_WRONG)'''
            
        # If user is already registered
        else:
            return messages.error(request, ErrorMessages.STUDENT_ALREADY_REGISTERED)