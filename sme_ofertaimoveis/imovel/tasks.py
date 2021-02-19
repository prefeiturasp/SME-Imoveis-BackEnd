from __future__ import absolute_import
import logging

from django.conf import settings
from celery import shared_task

from requests.exceptions import HTTPError

from ..dados_comuns.utils import send_email, consult_api_sciedu
from .models import Imovel, SME_Contatos

log = logging.getLogger(__name__)


@shared_task
def task_send_email_to_sme(imovel_id):
    emails = list((c.email for c in SME_Contatos.objects.get_contatos_ativos()))
    instance = Imovel.objects.get(pk=imovel_id)

    data = {"oferta": instance}
    demanda = []
    try:
        result = consult_api_sciedu(instance.latitude, instance.longitude)
        for grupo_id, grupo_name in settings.FILA_CRECHE_GRUPOS:
            faixa = next((x for x in result if x['cd_serie_ensino'] == grupo_id), None)
            demanda.append({"nome": grupo_name, "quantidade": faixa['total'] if faixa else 0})
    except HTTPError:
        pass
    data["demanda"] = demanda

    # Envia E-mail SME
    send_email(
        subject="Novo Cadastro de Oferta de Imóvel",
        template="email_to_sme",
        data=data,
        to_email=emails,
    )
    return "Email para A SME enviado com sucesso"

@shared_task
def task_send_email_to_usuario(email, imovel):
    send_email(
        subject=f"Assunto: Cadastro de imóvel – Protocolo nº {imovel['protocolo']} – Cadastro realizado.",
        template="email_to_usuario",
        data=imovel,
        to_email=email,
    )
    send_email(
        subject=f"Assunto: Cadastro de imóvel – Protocolo nº {imovel['protocolo']} – Cadastro realizado.",
        template="email_to_usuario",
        data=imovel,
        to_email='imoveis@sme.prefeitura.sp.gov.br',
    )

@shared_task
def send_email_(subject, template, data, to_email):
    send_email(
        subject=subject,
        template=template,
        data=data,
        to_email=to_email,
    )
