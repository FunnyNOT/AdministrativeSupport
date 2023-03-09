from django.db.models import Max

def class_profile_view(request, user_obj, group_obj, class_obj, member_obj, student_obj, student_grade_obj, logged_user_id, viewed_portal_id, viewed_class_id):

    # Get the student's group id
    student_group_id = group_obj.get(name='student').id

    # Get registered portal students
    portal_members = member_obj.filter(portal_id=viewed_portal_id, group_id=student_group_id, is_registered=True)

    # Get registered student usernames
    portal_member_username_list = portal_members.values_list('auth_user_id', flat=True)

    # Get the usernames of the portal_members based on id
    users_username_list = user_obj.filter(id__in=portal_member_username_list).values_list('username', flat=True)

    # Get the registered students of the class
    students = student_obj.filter(class_id_id=viewed_class_id, email__in=users_username_list)

    # Get the number of students in this class
    number_of_students = len(students)

    # Get the class record from database
    this_class = class_obj.get(id=viewed_class_id)

    # Get assigned teacher
    assigned_teacher = user_obj.filter(username=this_class.assigned_teacher)

    assigned_teacher_dict = {'first_name': assigned_teacher[0].first_name if assigned_teacher else '', 
                            'last_name': assigned_teacher[0].last_name if assigned_teacher else '',}
    
    if assigned_teacher:
        # Get if the assigned teacher is the logged_user
        if str(assigned_teacher[0].id) == str(logged_user_id):
            logged_is_assigned_teacher = True
        else:
            logged_is_assigned_teacher = False
    else:
        logged_is_assigned_teacher = False

    # Get list of students of this class
    class_students = student_obj.filter(class_id_id=viewed_class_id)
    
    # Get class student usernames into a list
    student_usernames_list = class_students.values_list('email', flat=True)

    # Get auth user students from this class
    auth_user_students_list = user_obj.filter(username__in=student_usernames_list).values_list('username', flat=True)

    # Get class students with email that exists in auth_user
    class_students = class_students.filter(email__in=auth_user_students_list)

    # Get class student ids into a list
    student_id_list = class_students.values_list('id', flat=True)

    # Get average list
    student_grade_list = student_grade_obj.filter(student_id__in=student_id_list)

    # Get the record with the highest average
    student_of_honor_grade_record = student_grade_list.order_by('-average_grade').first()

    # If student_of_honor_grade record exists 
    if student_of_honor_grade_record:

        this_student_record = student_obj.get(id=student_of_honor_grade_record.student_id)
        auth_user_this_student = user_obj.filter(username=this_student_record.email)
        this_student_grade_record = student_grade_obj.get(student_id=this_student_record.id)

        # Check if there is auth_user record for the student
        if auth_user_this_student:
            student_of_honor_dict = {'first_name': auth_user_this_student[0].first_name,
                                    'last_name': auth_user_this_student[0].last_name,
                                    'average_grade': student_of_honor_grade_record.average_grade}

    student_info_list = []

    # Get possible teachers for assigned teacher
    possible_assigned_teachers = member_obj.filter(portal_id=viewed_portal_id, group_id=4)
    possible_assigned_teacchers_ids_list = possible_assigned_teachers.values_list('auth_user_id', flat=True)
    possible_assigned_teachers_users = user_obj.filter(id__in=possible_assigned_teacchers_ids_list)

    possible_assigned_teachers_list = []
    for teacher in possible_assigned_teachers_users:

        possible_assigned_teachers_dict = {'id': teacher.id,
                                           'first_name': teacher.first_name,
                                           'last_name': teacher.last_name}

        possible_assigned_teachers_list.append(possible_assigned_teachers_dict)

    # Get student information into a dictionary
    for student in students:

        student_user = user_obj.get(username=student.email)

        student_grades = student_grade_obj.get(student_id=student.id)

        grades = eval(student_grades.grades)

        student_dict = {'id': student.id,
                        'first_name': student_user.first_name,
                        'last_name': student_user.last_name,
                        'email': student.email,
                        'absences': student.absences,
                        'maths': grades['maths'],
                        'physics': grades['physics'],
                        'chemistry': grades['chemistry'],
                        'english': grades['english'],
                        'geography': grades['geography'],
                        'history': grades['history'],
                        'biology': grades['biology'],
                        'average_grade': student_grades.average_grade
                        }

        student_info_list.append(student_dict)

    dict = {'number_of_students': number_of_students,
            'student_info': student_info_list,
            'assigned_teacher': assigned_teacher_dict,
            'student_of_honor': student_of_honor_dict if auth_user_this_student else None,
            'teacher_list': possible_assigned_teachers_list,
            'class_name': this_class.name,
            'class_id': viewed_class_id,
            'portal_id': viewed_portal_id,
            'logged_user_is_assigned_teacher': logged_is_assigned_teacher}

    return dict