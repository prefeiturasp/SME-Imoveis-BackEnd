import environ
import requests
from datetime import datetime

from des.models import DynamicEmailConfiguration

from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage
from django.conf import settings

from ..config.settings.base import URL_CONFIGS

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

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {settings.SCIEDU_TOKEN}"}
    url = (
        f"{settings.SCIEDU_URL}/{latitude}/{longitude}"
    )

    response = requests.request("GET", url, headers=headers)
    response.raise_for_status()
    return response.json()["results"]

def url_configs(variable, content):
    return env('REACT_APP_URL') + URL_CONFIGS[variable].format(**content)


def ofuscar_email(email):
    m = email.split('@')
    return f'{m[0][0]}{"*" * (len(m[0]) - 2)}{m[0][-1]}@{m[1]}'


class TerceirizadasClient:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {settings.EOL_API_TERCEIRIZADAS_TOKEN}"}
    
    url = f"{settings.EOL_API_TERCEIRIZADAS_URL}"
    
    @classmethod
    def dres(cls):
        response = requests.get(f"{cls.url}/dres", headers=cls.headers)
        response.raise_for_status()
        return response.json()["results"]

    @classmethod
    def subprefeituras(cls):
        response = requests.get(f"{cls.url}/subprefeituras", headers=cls.headers)
        response.raise_for_status()
        return response.json()["results"]

    @classmethod
    def distritos(cls):
        response = requests.get(f"{cls.url}/distritos", headers=cls.headers)
        response.raise_for_status()
        return response.json()["results"]

    @classmethod
    def setores(cls):
        response = requests.get(f"{cls.url}/setores", headers=cls.headers)
        response.raise_for_status()
        return response.json()["results"]

