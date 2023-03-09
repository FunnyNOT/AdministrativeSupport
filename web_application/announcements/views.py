from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User

from members.utils.basic_context import get_basic_context
from announcements.utils import announcements_list, announcements_create, announcements_edit, announcements_delete
from announcements.models import Announcement
from members.models import Member
from portals.models import Portal


# Create objects
announcements_obj = Announcement.objects
member_obj = Member.objects
portal_obj = Portal.objects
user_obj = User.objects

@permission_required("announcements.can_view_announcement")
def announcement_views(request):

    # Get logged user id
    logged_user_id = request.user.id

    # Get context basic
    context_b = get_basic_context(logged_user_id, search_bar=True)


    # GET request method
    if request.method == 'GET':
        
        announcements_context = announcements_list.announcements_list(request, user_obj, announcements_obj, member_obj, portal_obj, logged_user_id)

        context = {'context_basic': context_b, 'context_announcements': announcements_context}
    
        # Render the html template with the context of announcements
        return render(request, 'announcements.html', context)

    elif request.method == 'POST':

        logged_user_id = request.user.id
        
        # Get the action from the POST request
        announcements_action = request.POST.get('announcements_action')

        operation_dict = {
                "create_announcement": lambda: announcements_create.announcement_create(request, announcements_obj, member_obj, logged_user_id),
                "edit_announcement": lambda: announcements_edit.announcement_edit(request, announcements_obj, member_obj, logged_user_id),
                "delete_announcement": lambda: announcements_delete.announcement_delete(request, announcements_obj, member_obj, logged_user_id),
            }

        context_operational = operation_dict.get(announcements_action)()
        

        return redirect('Announcements')
