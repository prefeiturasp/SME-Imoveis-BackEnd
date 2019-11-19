from __future__ import absolute_import

from django.conf import settings
from celery import shared_task

from requests.exceptions import HTTPError

from ..dados_comuns.utils import send_email, consult_api_sciedu
from .models import Imovel, SME_Contatos


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
def task_send_email_to_usuario(email, protocolo=None):
    send_email(
        subject="Obrigado pelo envio do seu imóvel",
        template="email_to_usuario",
        data={'protocolo': protocolo},
        to_email=email,
    )
