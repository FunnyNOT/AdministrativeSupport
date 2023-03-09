from django.db import connection

def portal_view_list(request, portal_obj):

    q_generic = request.GET.get('search_value')

    # Query to get the data for the table with all the users
    query = 'Select a.name, a.users, a.is_active, a.id from portals as a'
    
    query += f' where a.name != "Admin Portal"'

    if q_generic:
        query += f' and a.name like "%{q_generic}%"'

    
            
    # Connect with the database
    with connection.cursor() as conn:

        conn.execute(query)
        results = conn.fetchall()

    final_info = []

    # Get the results inside of a list of dictionaries to send to the template
    for result in results:

        dict = {'id': result[3],
                'name': result[0],
                'users': result[1], 
                'is_active': result[2]}
                
        
        final_info.append(dict)

    return final_info





