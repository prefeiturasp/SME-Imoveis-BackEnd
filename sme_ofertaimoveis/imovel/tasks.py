from __future__ import absolute_import
import logging

from datetime import datetime
import requests

from django.conf import settings
from celery import shared_task

from requests.exceptions import HTTPError

from ..dados_comuns.utils import send_email, consult_api_sciedu
from .models import DemandaImovel, Imovel, SME_Contatos
from smtplib import SMTPServerDisconnected

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

@shared_task(
    autoretry_for=(SMTPServerDisconnected,),
    retry_backoff=2,
    retry_kwargs={'max_retries': 8},
)
def task_send_email_to_usuario(subject, template, data, email):
    sme_email = 'imoveis@sme.prefeitura.sp.gov.br'
    send_email(subject=subject, template=template, data=data, to_email=email)
    send_email(subject=subject, template=template, data=data, to_email=sme_email)

@shared_task
def send_email_(subject, template, data, to_email):
    send_email(
        subject=subject,
        template=template,
        data=data,
        to_email=to_email,
    )


@shared_task
def atualiza_demandas():
    for demanda_imovel in DemandaImovel.objects.all():
        imovel = demanda_imovel.imovel
        url = f'{settings.SCIEDU_URL}/{imovel.latitude}/{imovel.longitude}'
        headers = {
            "Authorization": f'Token {settings.SCIEDU_TOKEN}',
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        results = response.json().get('results')

        try:
            bercario_i = next(item for item in results if item["cd_serie_ensino"] == 1)
            demanda_imovel.bercario_i = bercario_i.get('total')
        except StopIteration:
            demanda_imovel.bercario_i = 0
        try:
            bercario_ii = next(item for item in results if item["cd_serie_ensino"] == 4)
            demanda_imovel.bercario_ii = bercario_ii.get('total')
        except StopIteration:
            demanda_imovel.bercario_ii = 0
        try:
            mini_grupo_i = next(item for item in results if item["cd_serie_ensino"] == 27)
            demanda_imovel.mini_grupo_i = mini_grupo_i.get('total')
        except StopIteration:
            demanda_imovel.mini_grupo_i = 0
        try:
            mini_grupo_ii = next(item for item in results if item["cd_serie_ensino"] == 28)
            demanda_imovel.mini_grupo_ii = mini_grupo_ii.get('total')
        except StopIteration:
            demanda_imovel.mini_grupo_ii = 0


        demanda_imovel.data_atualizacao = datetime.now()
        demanda_imovel.save()
