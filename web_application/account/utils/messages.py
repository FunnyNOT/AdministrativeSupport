class LoginMessages(object):
    
    WRONG_CREDENTIALS = 'Wrong credentials'
    ACCOUNT_INACTIVE = 'Account needs to be activated'
    INEXISTANT_ACCOUNT = "Account doesn't exist"
    PORTAL_INACTIVE = "User's portal is inactive"

    SUCCESSFUL_LOGIN = "Successful login"

class RegistrationMessages(object):

    EMPTY_FIRST_NAME = 'First name field cannot be empty'
    EMPTY_LAST_NAME = 'Last name field cannot be empty'
    EMPTY_EMAIL = 'Email field cannot be empty'
    EMPTY_PASSWORD = 'Password field cannot be empty'

    NOT_VALID_EMAIL = 'Email is not valid'
    EMAIL_NOT_INVITED = 'Email has not been invited to the platform'
    EMAIL_ALREADY_REGISTERED = 'Email has already been registered to the platform'

    NOT_VALID_PASSWORD = "Not valid password"
    PASSWORDS_DONT_MATCH = "Password and repeat password don't match"

class GenericMessages(object):
    
    SOMETHING_WENT_WRONG = 'Something went wrong, please contact support'