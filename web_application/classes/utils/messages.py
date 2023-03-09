class ErrorMessages(object):
    EMPTY_CLASS_NAME = 'Name field cannot be empty'
    CLASS_NAME_EXISTS = 'Class name already exists'
    NOTHING_CHANGED = 'Nothing Changed'
    MARK_FIELD_EMPTY = 'Cannot have empty mark fields'
    PERSONAL_FIELD_EMPTY = 'Cannot have empty personal fields'
    SOMETHING_WENT_WRONG = 'Something went wrong, please try again'
    EMAIL_EXISTS_IN_CLASS = 'Email already exists in this class'
    SELECT_STUDENT = 'Student must be selected'
    SELECT_TEACHER = 'Teacher must be selected'
    TEACHER_SELECTED_IS_THE_SAME = 'Teacher selected is already the assigned teacher'
    TEACHER_DOESNT_BELONG_TO_PORTAL = "Selected teacher doesn't belong to this portal"
    NOT_VALID_FILE = 'File type has to be PDF'
    NOT_VALID_FILE_SIZE = 'File size has to be below 10mb'
    EMPTY_FILE_INPUT = 'File has to be selected'
    STUDENT_ALREADY_REGISTERED = 'Student is already registered'


class SuccessMessages(object):
    SUCCESSFUL_ENTRY = 'Class created successfully'
    SUCCESSFUL_CLASS_EDIT = 'Successfully edited this class'
    SUCCESSFUL_STUDENT_ADDITION = 'Successfully added a student'
    SUCCESSFUL_STUDENT_EDIT = "Successfully edited a student's information"
    SUCCESSFUL_STATUS_CHANGE = 'Successfully change the activity of the portal'
    SUCCESSFUL_STUDENT_DELETE = "Successfully deleted a student"
    SUCCESSFUL_PORTAL_DELETE = 'Successfully deleted portal'
    SUCCESSFUL_ASSIGNED_TEACHER_EDIT = 'Successfully edited assigned teacher'
    SUCCESSFUL_STUDENT_INVITATION = 'Successul resent register invitation'
