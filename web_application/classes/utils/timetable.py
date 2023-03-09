import os
from config import PDF_URL

def timetable_view(request, viewed_portal_id, viewed_class_id):

    full_path = PDF_URL + '/' + viewed_portal_id + '_' + viewed_class_id + '_timetable.pdf'

    if os.path.exists(full_path):
        file_exists = True
    else:
        file_exists = False

    dict = {'portal_id': viewed_portal_id,
            'class_id': viewed_class_id,
            'file_exists': file_exists}


    return dict
            
