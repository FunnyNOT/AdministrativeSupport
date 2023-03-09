from homepage.templatetags.has_group import has_group

def member_profile_view(request, member_obj, user_obj, group_obj, portal_obj, class_obj, student_obj, viewed_user_id, logged_user_id):

    # Get the record from members table for viewed_user_id
    this_member = member_obj.get(auth_user_id=viewed_user_id)

    # Get the record from auth_user table for viewed_user_id
    this_user = user_obj.get(id=viewed_user_id)

    # Get the portal of the user
    this_portal = portal_obj.get(id=this_member.portal_id)

    # Check if logged_user_id == viewed_user_id
    if str(logged_user_id) == str(viewed_user_id):
        can_edit_flag = 1
    else:
        can_edit_flag = 0

    # Get the group of the user
    group = request.user.groups.values_list('name', flat=True)[0]

    # Get the classes this teacher is assigned at
    assigned_classes = class_obj.filter(assigned_teacher_id=viewed_user_id).values_list('name', flat=True)

    if has_group(request.user, ['student']):

        # Get the classes the student belongs
        this_student = student_obj.get(email=this_user.username)
        belongs_to_class = class_obj.get(id=this_student.class_id_id)
    

    # Create the dictionary for front_end
    dict = {'first_name': this_user.first_name,
            'last_name': this_user.last_name,
            'group': group,
            'portal': this_portal.name,
            'can_edit_flag': can_edit_flag,
            'assigned_classes': assigned_classes,
            'belongs_to_class': belongs_to_class.name if has_group(request.user, ['student']) else None,
            'email': this_user.username}




    return dict