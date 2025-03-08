import smtplib
from django.core.mail import send_mail
from django.conf import settings


def envoyer_email(email, code ,message):
    subject = "Email"
    body = f"{message} - {code}"
    email='mdval4194@gmail.com'
    try:
        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER, 
            [email],  
            fail_silently=False,
        )
        return True
    except Exception as e:
        return False