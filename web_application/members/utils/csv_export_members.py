import os
import csv
import mimetypes

from django.db import connection
from django.http import HttpResponse, Http404

from config import BASE_DIR

def csv_export_members(request):

    file_name = 'csv_export.csv'
    file_path = BASE_DIR + '/temp_files' + file_name

    with open(file_path, 'w', encoding='UTF8') as f:

        # Query to get the data for the table with all the users
        query ='Select a.username, a.first_name, a.last_name, a.is_superuser, a.is_active, c.name, d.name \
                from auth_user as a\
                inner join members as b on b.auth_user_id=a.id \
                inner join portals as c on b.portal_id=c.id \
                inner join auth_group as d on b.group_id=d.id'

        
        # Connect with the database
        with connection.cursor() as conn:

            conn.execute(query)
            results = conn.fetchall()


        header = ['email', 'first_name', 'last_name', 'is_superuser', 'is_active', 'portal_name', 'role']

        writer = csv.writer(f)

        writer.writerow(header)

        for result in results:
            writer.writerow(result)


    # Open the file for reading content
    path = open(file_path, 'rb')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(file_path)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % file_name
    # Return the response value
    return response
    



        

        