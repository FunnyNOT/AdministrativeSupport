from datetime import datetime
import pytz

from django.db import connection

from members.utils.event_types import EventTypes


def dashboard_admin_view(portal_obj, analytics_members_obj):

    dict = {}

    # Get the number of active portals
    number_of_active_portals = portal_obj.filter(is_active=1).exclude(name='Admin Portal').count()


    # Get the portals with most logins this month
    query = f"select a.portal_id, b.name, count(*) as logins\
            from analytics_members as a inner join portals as b on a.portal_id=b.id\
                 where a.event_type='{EventTypes.LOGIN}' and not b.name = 'Admin Portal'\
                     group by a.portal_id\
                         order by logins desc LIMIT 3;"
    
    with connection.cursor() as conn:
        conn.execute(query)
        results = conn.fetchall()
    
    # Get the last 3 active portals created
    latest_created = portal_obj.filter(is_active=1).exclude(name='Admin Portal').order_by('-created_at')[:3].values_list('name', flat=True)
    
    # Append the dictionary with key: value pairs

    dict['number_of_active_portals'] = number_of_active_portals

    dict['latest_portals'] = latest_created

    dict['most_login_portals'] = []
    for record in results:
        dict['most_login_portals'].append({'portal_id': record[0],
                                           'portal_name': record[1],
                                           'number_of_logins': record[2]})

    return dict