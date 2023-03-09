from homepage.templatetags.has_group import has_group

def class_view_list(request, user_obj, class_obj, member_obj, student_obj, logged_user_id, viewed_portal_id):

    # Get the members record from Member table
    viewed_member = member_obj.get(auth_user_id=logged_user_id)

    if has_group(request.user, ['student']):

        auth_user_this_student = user_obj.get(id=logged_user_id)

        # Get the student's class
        this_student = student_obj.get(email=auth_user_this_student.username)

        #
        classes = class_obj.filter(id=this_student.class_id_id)

    else:
        # Get the classes that belong to the user's portal
        classes = class_obj.filter(portal_id=viewed_portal_id)
    


    context = []

    # Loop through classes to get their information
    for single_class in classes:
        
        # Get the students that belong to the portal
        students = student_obj.filter(class_id_id=single_class.id)

        # Get the student auth_user_id list
        student_email_list = students.values_list('email', flat=True)

        # Get the auth user records of these students
        students_auth_user_list = user_obj.filter(username__in=student_email_list)

        dict =  {'class_id': single_class.id,
                 'class_portal_id': viewed_portal_id,
                 'class_name': single_class.name,
                 'number_of_students': str(len(students_auth_user_list))}
                
        context.append(dict)


    return context
    


    