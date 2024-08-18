from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage, send_mail
from decouple import config
from django.conf import settings

def  send_confirmation_mail(user):
    try:
        mail_subject = 'Activate your blog account.'
        print(1)
        message = render_to_string('confirmation_email.html', {
            'user': user,
            'domain': config("DOMAIN"),
            'uid':urlsafe_base64_encode(force_bytes(user.id)),
            'token':account_activation_token.make_token(user),
        })
        print(2)
        from_email=settings.EMAIL_HOST_USER
        print(from_email)
        to_email = user.email
        print(to_email)
        # send_mail(subject=mail_subject, message=message, from_email=from_email, recipient_list=to_email, fail_silently=False)
        email = EmailMessage(
                    mail_subject, message, from_email=from_email,to=[to_email]
        )
        email.content_subtype = "html"
        email.send()
        return True
    except Exception as e:
        return e

def activate_user(user, token):
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return True
    else:
        return False