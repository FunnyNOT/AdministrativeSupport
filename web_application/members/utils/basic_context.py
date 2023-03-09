from django.db import connection

from members.models import Member
from portals.models import Portal

def get_basic_context(logged_user_id, **kwargs):

    basic_context_dict = {}

    # Get first_name, last_name, portal of logged user
    query = f'select c.first_name, c.last_name, b.name, b.id, a.auth_user_id from members as a \
        inner join portals as b on a.portal_id = b.id\
        inner join auth_user as c on a.auth_user_id = c.id\
                  where a.auth_user_id = "{logged_user_id}"'
    
    with connection.cursor() as conn:
            conn.execute(query)
            records = conn.fetchall()


    basic_context_dict = {'first_name': records[0][0],
                          'last_name': records[0][1],
                          'portal': records[0][2],
                          'portal_id': records[0][3],
                          'user_id': records[0][4],
                          'search_bar': True if 'search_bar' in kwargs else False}
    

    return basic_context_dict
