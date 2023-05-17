from .models import User
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.db.models.base import ModelBase



class ActiveAccount:
    def __init__(self, user: User) -> None:
        if not isinstance(user, User):
            raise ValueError('user must be a User instance')
        self._user = user
    
    def _generate_url(self) -> str:
        protocol = 'http' if settings.DEBUG else 'https'
        domain = settings.DOMAIN
        uid = urlsafe_base64_encode(force_bytes(self._user.pk))
        token = default_token_generator.make_token(self._user)
        return f'{protocol}://{domain}{reverse("active_account", kwargs={"uidb4": uid, "token": token})}'
    
    def active_account_send_email(self) -> None:
        active_url = self._generate_url()
        mail_subject = 'Activate your account on EDIV'
        mail_body = render_to_string('mails/active_account.html', {'active_url': active_url})
        email = EmailMessage(mail_subject, mail_body, to=[self._user.email])
        if email.send():
            # TODO: ADD LOG SUCCESS
            pass
        else:
            # TODO: ADD LOG ERROR
            pass
        