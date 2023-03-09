# Django imports
from django.db import migrations
from django.contrib.auth.models import Group



def forwards_func(apps, schema_editor):
    '''
    Function that initiates the databse with a System Admin, Admin and a Teacher
    '''
    group_obj = Group.objects
    
    group_entries = [
        {'name': 'system_admin'},
        {'name': 'admin'},
        {'name': 'manager'},
        {'name': 'teacher'},
        {'name': 'student'}
    ]

    
    # Initiate Group entries
    #for entry in group_entries:
        #group_obj.create(name=entry['name'])
                            

class Migration(migrations.Migration):

    dependencies = [
       ('members','0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func)
    ]
