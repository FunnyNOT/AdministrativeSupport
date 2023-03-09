from datetime import datetime
from xml.dom.expatbuilder import parseString
import pytz
import pandas as pd

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.db import transaction

from members.models import Member, AllowMemberRegistration
from portals.models import Portal
from announcements.models import Announcement
from events.models import Event
from classes.models import Class, Student, StudentGrade
from config import STATIC_CSV


class Command(BaseCommand):


    def handle(self, *args, **options):

        # Get datetime now
        datetime_now = datetime.utcnow().replace(tzinfo=pytz.UTC)

        member_obj = Member.objects
        allow_member_obj = AllowMemberRegistration.objects
        user_obj = User.objects
        portal_obj = Portal.objects
        group_obj = Group.objects
        announcement_obj = Announcement.objects
        event_obj = Event.objects
        class_obj = Class.objects
        student_obj = Student.objects
        student_grade_obj = StudentGrade.objects

        df_announcements = pd.read_csv(STATIC_CSV + '/announcements.csv')
        df_members = pd.read_csv(STATIC_CSV + '/members.csv')
        df_classes = pd.read_csv(STATIC_CSV + '/classes.csv')
        df_events = pd.read_csv(STATIC_CSV + '/events.csv')
        df_portals = pd.read_csv(STATIC_CSV + '/portals.csv')
        df_students = pd.read_csv(STATIC_CSV + '/students.csv')
        df_students_grades = pd.read_csv(STATIC_CSV + '/students_grades.csv')

        def fill_allow_member_registration(df_members, allow_member_obj):


            for index, row in df_members.iterrows():

                allow_member_obj.create(id=index+1, 
                                        username=row['username'], 
                                        created_date=row['date_joined'], 
                                        last_updated_date=row['date_joined'],
                                        is_registered=row['is_registered'],
                                        invitation_counter=1,
                                        group_id=row['group_id'],
                                        portal_id=row['portal_id'])

        def fill_auth_user(df_members, user_obj):

            for index, row in df_members.iterrows():

                user_obj.create(id=index+1, 
                                password=make_password(row['password']),
                                is_superuser=row['is_superuser'],
                                username=row['username'],
                                first_name=row['first_name'],
                                last_name=row['last_name'],
                                email=row['email'],
                                is_staff=1,
                                date_joined=row['date_joined'],
                                is_active=1
                )

                # Get the group
                group = group_obj.get(id=row['group_id'])
                
                # Assign group to the user
                group.user_set.add(index+1)

        def fill_members(df_members, member_obj, portal_obj):

             for index, row in df_members.iterrows():

                member_obj.create(id=index+1,
                                is_registered=row['is_registered'],
                                created_at=row['date_joined'],
                                group_id=row['group_id'],
                                portal_id=row['portal_id'],
                                auth_user_id=index+1
                                )

                # Update users in portal table                                
                portal = portal_obj.get(id=row['portal_id'])
                portal.users = portal.users + 1
                portal.save()

        def fill_portals(df_portals, portal_obj):
            
            for index, row in df_portals.iterrows():

                portal_obj.create(id=index+1,
                                  name=row['name'],
                                  is_active=row['is_active'], 
                                  created_at=datetime_now)

        def fill_announcements(df_announcements, announcement_obj):

            for index, row in df_announcements.iterrows():

                announcement_obj.create(id=index+1,
                                        title=row['title'],
                                        body=row['body'],
                                        is_active=row['is_active'], 
                                        visible_to_students=row['visible_to_students'],
                                        created_at=datetime_now,
                                        created_by_id=row['created_by_id'],
                                        portal_id=row['portal_id'])

        def fill_events(df_events, event_obj):

            for index, row in df_events.iterrows():

                event_obj.create(id=index+1,
                                        title=row['title'],
                                        description=row['description'],
                                        is_active=row['is_active'],
                                        visible_to_students=row['visible_to_students'],
                                        event_datetime=row['event_datetime'],
                                        created_at=datetime_now,
                                        created_by_id=row['created_by_id'],
                                        portal_id=row['portal_id'])
        
        def fill_classes(df_classes, class_obj):
            for index, row in df_classes.iterrows():

                class_obj.create(id=index+1,
                                name=row['name'],
                                created_at=row['created_at'],
                                created_by_id=row['created_by_id'],
                                assigned_teacher_id=row['assigned_teacher'],
                                portal_id=row['portal_id'])
        
        def fill_students(df_students, student_obj):

            for index, row in df_students.iterrows():
                
                this_class = class_obj.get(id=row['class_id'])

                allow_member_obj.create(username=row['email'], 
                                        created_date=datetime_now, 
                                        last_updated_date=datetime_now,
                                        is_registered=True,
                                        invitation_counter=1,
                                        group_id=5,
                                        portal_id=this_class.portal_id)
                
                user_obj.create(password=make_password(row['password']),
                                is_superuser=0,
                                username=row['email'],
                                first_name=row['fname'],
                                last_name=row['lname'],
                                email=row['email'],
                                is_staff=1,
                                date_joined=datetime_now,
                                is_active=1
                )

                # Get the group
                group = group_obj.get(id=5)

                # Get the user from auth_user
                this_user = user_obj.get(email=row['email'])

                # Assign group to the user
                group.user_set.add(this_user.id)

                member_obj.create(is_registered=True,
                                created_at=datetime_now,
                                group_id=5,
                                portal_id=this_class.portal_id,
                                auth_user_id=this_user.id
                                )


                student_obj.create(email=row['email'],
                                   belongs_to_class=row['belongs_to_class'],
                                   absences=row['absences'],
                                   class_id_id=row['class_id']
                            )

                this_portal = portal_obj.get(id=this_class.portal_id)
                this_portal.users = int(this_portal.users) + 1
                this_portal.save()

        def fill_student_grades(df_students_grades, student_grade_obj):

            for index, row in df_students_grades.iterrows():
                maths = row['maths']
                physics = row['physics']
                chemistry = row['chemistry']
                english = row['english']
                geography = row['geography']
                history = row['history']
                biology = row['biology']

                list = [maths, physics, chemistry, english, geography, history, biology]
                dict = {'maths': maths,
                        'physics': physics,
                        'chemistry': chemistry,
                        'english': english,
                        'geography': geography,
                        'history': history,
                        'biology': biology
                        }
                # Get the average of the subjects
                average = sum(list)/len(list)

                student_grade_obj.create(grades=dict,
                                         average_grade=average,
                                         student_id = row['student_id']
                                        )

        def fill_analytics_members():

            pass



        with transaction.atomic():
            print('***Start importing portals***')
            fill_portals(df_portals, portal_obj)
            print('***Start importing member_registrations***')
            fill_allow_member_registration(df_members, allow_member_obj)
            print('***Start importing auth_user***')
            fill_auth_user(df_members,user_obj)
            print('***Start importing members***')
            fill_members(df_members, member_obj, portal_obj)
            print('***Start importing announcements***')
            fill_announcements(df_announcements, announcement_obj)
            print('***Start importing events***')
            fill_events(df_events, event_obj)
            print('***Start import classes***')
            fill_classes(df_classes, class_obj)
            print('***Start importing students***')
            fill_students(df_students, student_obj)
            print('***Start importing student grades***')
            fill_student_grades(df_students_grades, student_grade_obj)

