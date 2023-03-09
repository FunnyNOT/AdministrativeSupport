import os
from datetime import datetime
from re import A
from tkinter import E
import pytz

from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.db import transaction

from classes.utils.messages import ErrorMessages, SuccessMessages
from config import PDF_URL

def file_upload(request, class_obj, member_obj, viewed_portal_id, viewed_class_id, logged_user_id):

    new_file = request.FILES['timetable_pdf'] if request.FILES else None
    
    # Check file not empty
    if not new_file:
        return messages.error(request, ErrorMessages.EMPTY_FILE_INPUT)

    # Check valid pdf file
    if not new_file.name.endswith('.pdf'):
        return messages.error(request, ErrorMessages.NOT_VALID_FILE)

    # Check valid size
    if new_file.size>10000000:
        return messages.error(request, ErrorMessages.NOT_VALID_FILE_SIZE)


    # Save the file in directory
    fs = FileSystemStorage(location=PDF_URL)

    full_file_path = PDF_URL + '/' + str(viewed_portal_id) + '_' + str(viewed_class_id) + '_timetable.pdf'
    
    if os.path.exists(full_file_path):
        os.remove(full_file_path)

    full_name = str(viewed_portal_id) + '_' + str(viewed_class_id) + '_timetable.pdf'
    
    fs.save(full_name, new_file)
