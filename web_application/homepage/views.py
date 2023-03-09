from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from members.utils.basic_context import get_basic_context
from homepage.templatetags.has_group import has_group
from homepage.utils.dashboard_admin_view import dashboard_admin_view
from homepage.utils.dashboard_users_view import dashboard_users_view

from portals.models import Portal
from members.models import AnalyticsMembers
from announcements.models import Announcement
from events.models import Event
from members.models import Member


portals_obj = Portal.objects
analytics_members_obj = AnalyticsMembers.objects
announcements_obj = Announcement.objects
member_obj = Member.objects
event_obj = Event.objects

@login_required
def homepage_view(request):

    logged_user_id = request.user.id

    context_b = get_basic_context(logged_user_id)

    context = {'context_basic': context_b}

    if has_group(request.user, ['admin', 'system_admin']):

        context_admin = dashboard_admin_view(portals_obj, analytics_members_obj)

        context = {'context_basic': context_b, 'context_admin': context_admin}
        
        return render(request, 'homepage_admin.html', context)
    else:

        context_users = dashboard_users_view(request, announcements_obj, member_obj, event_obj, logged_user_id)

        context = {'context_basic': context_b, 'context_users': context_users}

        return render(request, 'homepage.html', context)
