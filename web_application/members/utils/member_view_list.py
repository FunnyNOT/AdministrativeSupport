from django.db import connection


def members_view_list(request, member_obj):

    q_generic = request.GET.get('search_value')

    # Query to get the data for the table with all the users
    query = 'Select a.username, a.first_name, a.last_name, a.is_superuser, a.is_active, c.name, d.name \
            from auth_user as a\
            inner join members as b on b.auth_user_id=a.id \
            inner join portals as c on b.portal_id=c.id \
            inner join auth_group as d on b.group_id=d.id'

    if q_generic:
        query += f' where a.first_name like "%{q_generic}%" or a.last_name like "%{q_generic}%" or c.name like "%{q_generic}%" or d.name like "%{q_generic}%"'
            
    # Connect with the database
    with connection.cursor() as conn:

        conn.execute(query)
        results = conn.fetchall()

    final_info = []

    # Get the results inside of a list of dictionaries to send to the template
    for result in results:

        if result[4] == 1:
            activity = 'Active'
        else:
            activity = 'Inactive'

        dict = {'email': result[0],
                'first_name': result[1],
                'last_name': result[2],
                'is_active': activity,
                'portal': result[5],
                'group': result[6],
                }
        
        final_info.append(dict)

    return final_info


def invitation_modal(request, portal_obj, group_obj, user_obj):
    
    modal_dict = {}

    # Get logged user id
    logged_user_id = request.user.id

    this_user = user_obj.get(id=logged_user_id)    

    if this_user.is_superuser == 1:

        # Get all the distinct portal names
        portals = portal_obj.all().values_list('name', flat=True)

    else:
        portals = portal_obj.all().exclude(name__in=['Admin Portal']).values_list('name', flat=True)

    
    # Get all the distinct group names
    groups = group_obj.all().exclude(name__in=['system_admin', 'student']).values_list('name', flat=True)


    modal_dict = {'portals': portals, 'groups': groups}


    return modal_dict