from django.db.models import Q
from homepage.templatetags.has_group import has_group


def evevts_view(request, user_obj, event_obj, member_obj, portal_obj, logged_user_id):

    search_input = request.GET.get('search_value')

    # Get the logged user record from members table
    logged_member = member_obj.get(auth_user_id=logged_user_id)
    
    if search_input is not None:

        # Check if the user is admin or system_admin
        if has_group(request.user, ['admin', 'system_admin']):
            # Get the announcements of all portals ordered
            events = event_obj.filter(is_active=1).order_by('-created_at')

            # Filter based on the search_input
            events = events.filter(Q(title__icontains=search_input) | Q(description__icontains=search_input))

        elif has_group(request.user, ['manager', 'teacher']):
            # Get the announcements from the portal of the user + the admin portal
            events = event_obj.filter(portal_id__in=[logged_member.portal_id, 1], is_active=1).order_by('-created_at')

            # Filter based on the search input
            events = events.filter(Q(title__icontains=search_input) | Q(description__icontains=search_input))
        
        elif has_group(request.user, ['student']):
            # Get the announcements from the portal of the user + the admin portal
            events = event_obj.filter(portal_id__in=[logged_member.portal_id, 1], is_active=1, visible_to_students=True).order_by('-created_at')

            # Filter based on the search input
            events = events.filter(Q(title__icontains=search_input) | Q(description__icontains=search_input))

    else:
        # Check if the user is admin or system_admin
        if has_group(request.user, ['admin', 'system_admin']):
            # Get the announcements of all portals
            events = event_obj.filter(is_active=1).order_by('-created_at')
        elif has_group(request.user, ['manager', 'teacher']):
            # Get the announcements from the portal of the user + the admin portal
            events = event_obj.filter(portal_id__in=[logged_member.portal_id, 1], is_active=1).order_by('-created_at')
        elif has_group(request.user, ['student']):
            # Get the announcements from the portal of the user + the admin portal
            events = event_obj.filter(portal_id__in=[logged_member.portal_id, 1], is_active=1, visible_to_students=True).order_by('-created_at')


    context_list = []

    for event in events:

        user = user_obj.get(id=event.created_by_id)
        portal = portal_obj.get(id=event.portal_id)
        
        dict = {'id': event.id,
                'title': event.title,
                'description': event.description,
                'event_datetime': event.event_datetime,
                'events_datetime': event.event_datetime.isoformat(),
                'is_active': event.is_active,
                'visible_to_students': event.visible_to_students,
                'created_at': event.created_at,
                'created_by_first_name': user.first_name,
                'created_by_last_name': user.last_name,
                'portal_name': portal.name,
        }

        context_list.append(dict)

    return context_list



