from homepage.templatetags.has_group import has_group

def dashboard_users_view(request, announcements_obj, member_obj, event_obj, logged_user_id):


    if has_group(request.user, ['student']):
        member = member_obj.get(auth_user_id=logged_user_id)
        announcements = announcements_obj.filter(portal_id__in=[member.portal_id, 1], is_active=1, visible_to_students=True).order_by('-created_at')[:2]
        events = event_obj.filter(portal_id__in=[member.portal_id, 1], is_active=1, visible_to_students=True).order_by('-created_at')[:2]

    else:
        member = member_obj.get(auth_user_id=logged_user_id)
        announcements = announcements_obj.filter(portal_id__in=[member.portal_id, 1], is_active=1).order_by('-created_at')[:2]
        events = event_obj.filter(portal_id__in=[member.portal_id, 1], is_active=1).order_by('-created_at')[:2]
    
    
    final_context = {}
    announcements_context = []
    events_context = []
    for announcement in announcements:

        dict = {'title': announcement.title,
                'body': announcement.body}

        
        announcements_context.append(dict)

    for event in events:
        dict = {'title': event.title,
                'description': event.description,
                'event_datetime': event.event_datetime
                }

        events_context.append(dict)


    final_context['announcements'] = announcements_context
    final_context['events'] = events_context
    
    return final_context 