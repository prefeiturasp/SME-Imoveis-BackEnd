import environ
import requests

from des.models import DynamicEmailConfiguration

from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage
from django.conf import settings

from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMultiAlternatives

env = environ.Env()


def send_email(subject, template, data, to_email):
    config = DynamicEmailConfiguration.get_solo()

    if not isinstance(to_email, list):
        to_email = [to_email]

    data["URL_HOSTNAME"] = settings.URL_HOSTNAME
    data["URL_HOSTNAME_WITHOUT_SLASH_API"] = env('URL_HOSTNAME_WITHOUT_SLASH_API')

    msg_html = render_to_string(f"imovel/html/{template}.html", data)
    msg = EmailMessage(
        subject=subject, body=msg_html, 
        from_email=config.from_email or None,
        bcc=to_email,
    )
    msg.content_subtype = "html"  # Main content is now text/html
    return msg.send()
    

def consult_api_fila_creche(latitude, longitude, grupo):

    headers = {"Content-Type": "application/json"}
    url = (
        f"{settings.FILA_CRECHE_URL}"
        f"/api/v1/schools/radius/wait"
        f"/{longitude}/{latitude}/{grupo}"
    )

    response = requests.request("GET", url, headers=headers)
    response.raise_for_status()
    return response.json()["results"]


def consult_api_sciedu(latitude, longitude):

    headers = {"Content-Type": "application/json", "Authorization": "Token 4fcce3bb12805893514061555474d867adc85329"}
    url = (
        f"{settings.SCIEDU_URL}"
        f"/imoveis/demanda"
        f"/{latitude}/{longitude}"
    )

    response = requests.request("GET", url, headers=headers)
    response.raise_for_status()
    return response.json()["results"]
