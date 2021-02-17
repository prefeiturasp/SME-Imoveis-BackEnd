from __future__ import absolute_import

import logging

from celery import shared_task
from django.conf import settings

from sme_ofertaimoveis.dados_comuns.services import atualiza_dados_comuns

log = logging.getLogger(__name__)


@shared_task
def task_atualiza_dados_comuns():
    log.info("Atualiza dados.")
    response = atualiza_dados_comuns()

    return response