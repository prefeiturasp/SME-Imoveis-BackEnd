from __future__ import absolute_import

from django.conf import settings
from celery import shared_task

from requests.exceptions import HTTPError

from ..dados_comuns.utils import send_email, consult_api_fila_creche
from .models import Imovel, SME_Contatos


@shared_task
def task_send_email_to_sme(imovel_id):

    emails = list((c.email for c in SME_Contatos.objects.get_contatos_ativos()))
    instance = Imovel.objects.get(pk=imovel_id)

    data = {"oferta": instance}
    demanda = []
    for grupo_id, grupo_name in settings.FILA_CRECHE_GRUPOS:
        try:
            result = consult_api_fila_creche(
                instance.latitude, instance.longitude, grupo_id
            )
            demanda.append({"nome": grupo_name, "quantidade": result["wait"]})

        except (HTTPError, KeyError) as ex:
            demanda.append({"nome": grupo_name, "quantidade": 0})
    data["demanda"] = demanda

    # Envia E-mail SME
    send_email(
        subject="Novo Cadastro de Oferta de Imovel",
        template="email_to_sme",
        data=data,
        to_email=emails,
    )
    return "Email para A SME enviado com sucesso"
