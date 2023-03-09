from django.core.mail import get_connection, EmailMessage
from email_configuration import EmailConfiguration


class Email(object):
    subject = None
    body = None
    email_sender = None
    email_attachment_data = None
    email_recipient = None

    def __init__(self,
                 subject=None,
                 body=None,
                 email_sender=None,
                 email_attachment_data=None,
                 email_recipient=None,
                 ):

        self.subject = subject
        self.body = body
        self.email_sender = email_sender
        self.email_attachment_data = email_attachment_data
        self.email_recipient = email_recipient


    def send_email(self):
        
        with get_connection(host=EmailConfiguration.HOST,
                            port=EmailConfiguration.PORT, 
                            username=EmailConfiguration.USERNAME, 
                            password=EmailConfiguration.PASSWORD, 
                            use_tls=EmailConfiguration.MY_USE_TLS,
                            ) as connection:

            EmailMessage(self.subject, self.body, EmailConfiguration.USERNAME, [self.email_recipient], connection=connection).send()
