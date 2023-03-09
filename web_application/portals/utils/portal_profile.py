from django.db import connection

def portal_profile_view(request, viewed_portal_id, user_obj, portal_obj, member_obj, group_obj, member_analytics_obj, announcement_obj, event_obj):

    # Get the viewed portal info
    portal_info = portal_obj.get(id=viewed_portal_id)

    # Get info of member table of the portal
    members_info = member_obj.filter(portal_id=viewed_portal_id)

    member_auth_id_list = members_info.values_list('auth_user_id', flat=True)

    auth_user_info = user_obj.filter(id__in=member_auth_id_list)

    # Get the number of manager of the portal
    managers = members_info.filter(group_id=3, is_registered=1).count()

    # Get the number of teachers of the portal
    teachers = members_info.filter(group_id=4, is_registered=1).count()
    
    # Get the number of students of the portal
    students = members_info.filter(group_id=5, is_registered=1).count()

    # Get the user with the most login inside the portal
    most_logins_query = f"SELECT auth_user_id, COUNT(event_type) as number FROM analytics_members where portal_id={viewed_portal_id} and event_type='login' GROUP BY auth_user_id order by number desc"
    
    # Get the number of announcements for this portal
    number_of_announcements = announcement_obj.filter(portal_id=viewed_portal_id).count()

    # Get the number of eventse for this portal
    number_of_events = event_obj.filter(portal_id=viewed_portal_id).count()

    # Connect with the database
    with connection.cursor() as conn:

        conn.execute(most_logins_query)
        results = conn.fetchall()
    

    # Initiate the dictionary to return values in front-end
    dict = {}

    # Get the generic info inside a dictionary
    dict['portal_info'] = {'id': portal_info.id,
                           'name': portal_info.name,
                           'users': portal_info.users,
                           'is_active': portal_info.is_active,
                           'managers': managers,
                           'teachers': teachers,
                           'students': students,
                           'announcements_number': number_of_announcements,
                           'events_number': number_of_events,
                           }
                           
    # If users from this portal have logged in                                     
    if results:
        most_login_user = user_obj.filter(id=results[0][0])[0]

        dict['portal_info']['most_logins'] = {'first_name': most_login_user.first_name,
                                              'last_name': most_login_user.last_name,
                                              'login_number': results[0][1]}

    # Get the user info inside a dictionary
    dict['user_info'] = []
    for user in auth_user_info:
        
        group = group_obj.filter(user=user.id)[0]

        dict['user_info'].append({'first_name': user.first_name,
                                  'last_name': user.last_name,
                                  'group_name': group})

    return dict