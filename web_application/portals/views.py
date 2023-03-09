from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import permission_required

from portals.utils.portal_create import portal_create
from portals.utils.portal_edit import portal_edit
from portals.utils.portal_view_list import portal_view_list
from portals.utils.portal_status_change import portal_status_change
from portals.utils.portal_profile import portal_profile_view
from portals.utils.portal_delete import portal_delete
from portals.models import Portal
from announcements.models import Announcement
from events.models import Event
from members.models import Member, AnalyticsMembers, AllowMemberRegistration
from members.utils.basic_context import get_basic_context

# Create your views here.
portal_obj = Portal.objects
member_obj = Member.objects
group_obj = Group.objects
member_analytics_obj = AnalyticsMembers.objects
user_obj = User.objects
allow_mbr_registration_obj = AllowMemberRegistration.objects
event_obj = Event.objects
announcement_obj = Announcement.objects

@permission_required("portals.view_portal")
def portal_view(request):

    logged_user_id = request.user.id

    # Get context basic
    context_b = get_basic_context(logged_user_id, search_bar=True)

    if request.method == 'POST':

        # Get the action from the POST request
        portals_action = request.POST.get('portals_action')

        operation_dict = {
                "create_portal": (lambda: portal_create(request, portal_obj), 'auth.can_create_portal'),
                "change_status": (lambda: portal_status_change(request, portal_obj), 'auth.can_change_portal_status'),
            }

        context_operational = operation_dict.get(portals_action)[0]() if request.user.has_perm(operation_dict.get(portals_action)[1]) else None
        
        # If it is a successful message redirect to Files library view
        if context_operational is None:
            return redirect("Portals")

        # Get portal_view_list after the creation of portal
        context_portal_view = portal_view_list(request, portal_obj)
            
        context = {'context_basic': context_b, 'portal_view': context_portal_view, 'context_operational': context_operational}

        return render(request, 'portal_list.html', context)
    
    elif request.method == 'GET':

        context_portal_view = portal_view_list(request, portal_obj)

        context = {'context_basic': context_b, 'portal_view': context_portal_view}

        return render(request, 'portal_list.html', context)

@permission_required("portals.can_view_portal_profile")
def portal_profile(request, viewed_portal_id):
    
    if request.method == 'GET':

        logged_user_id = request.user.id

        # Get context basic
        context_b = get_basic_context(logged_user_id)

        context_portal_profile = portal_profile_view(request, viewed_portal_id, user_obj, portal_obj, member_obj, group_obj, member_analytics_obj, announcement_obj, event_obj)

        context = {'context_basic': context_b, 'context_profile': context_portal_profile}

        return render(request, 'portal_profile.html', context)


    elif request.method == 'POST':

        # Get the action from the POST request
        portals_action = request.POST.get('portal_action')
        
        operation_dict = {
                "edit_portal": lambda: portal_edit(request, viewed_portal_id, portal_obj),
                "delete_portal": lambda: portal_delete(request, viewed_portal_id, portal_obj, user_obj, member_obj, allow_mbr_registration_obj),
            }

        context_operational = operation_dict.get(portals_action)()
        

        if context_operational is None:
            return redirect('Portal profile', viewed_portal_id=str(viewed_portal_id))

        else:
            # If the viewed portal is deleted redirect to Portals list page instead
            return redirect('Portals')
