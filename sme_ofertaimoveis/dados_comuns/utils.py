from des.models import DynamicEmailConfiguration
from django.core.mail import send_mail


def send_email(subject, message_text, to_email):
    config = DynamicEmailConfiguration.get_solo()
    send_mail(
        subject,
        message_text,
        config.from_email or None,
        [to_email])
