from django.db import migrations
from django.apps.registry import Apps, apps as global_apps
from django.contrib.contenttypes.management import create_contenttypes
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, Group


def forwards_func(apps, schema_editor):

    # Get or Create User groups
    if Group.objects.filter(name='system_admin').exists():
        system_admin_group = Group.objects.get(name='system_admin')
    else:
        system_admin_group = Group.objects.create(name='system_admin')

    if Group.objects.filter(name='admin').exists():
        admin_user_group = Group.objects.get(name='admin')
    else:
        admin_user_group = Group.objects.create(name='admin')

    if Group.objects.filter(name='manager').exists():
        manager_user_group = Group.objects.get(name='manager')
    else:
        manager_user_group = Group.objects.create(name='manager')

    if Group.objects.filter(name='teacher').exists():
        teacher_user_group = Group.objects.get(name='teacher')
    else:
        teacher_user_group = Group.objects.create(name='teacher')

    if Group.objects.filter(name='student').exists():
        student_user_group = Group.objects.get(name='student')
    else:
        student_user_group = Group.objects.create(name='student')


    my_app_config = global_apps.get_app_config('portals')
    create_contenttypes(my_app_config)

    auth_user_content_type = ContentType.objects.get(app_label='portals', model='portal')

    # Can View Portals
    can_view_portals = Permission(name='Can view portal', codename='can_view_portal',
                                content_type=auth_user_content_type)
    can_view_portals.save()
    system_admin_group.permissions.add(can_view_portals)
    admin_user_group.permissions.add(can_view_portals)

    # Can View Portal profile
    can_view_portal_profile =  Permission(name='Can view portal profile', codename='can_view_portal_profile',
                               content_type=auth_user_content_type)
    can_view_portal_profile.save()
    system_admin_group.permissions.add(can_view_portal_profile)
    admin_user_group.permissions.add(can_view_portal_profile)
    manager_user_group.permissions.add(can_view_portal_profile)
    teacher_user_group.permissions.add(can_view_portal_profile)
    student_user_group.permissions.add(can_view_portal_profile)

class Migration(migrations.Migration):


    dependencies = [
        ('portals','0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func)
        ]