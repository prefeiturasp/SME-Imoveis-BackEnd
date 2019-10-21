from des.models import DynamicEmailConfiguration

from django.template.loader import render_to_string
from django.core.mail import send_mail

from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMultiAlternatives


def send_email(subject, template, data, to_email):
    config = DynamicEmailConfiguration.get_solo()

    if not isinstance(to_email, list):
        to_email = [to_email]

    msg_plain = render_to_string(
        f'imovel/txt/{template}.txt', data)
    msg_html = render_to_string(
        f'imovel/html/{template}.html', data)

    send_mail(
        subject,
        msg_plain,
        config.from_email or None,
        to_email,
        html_message=msg_html
    )
