from concurrent import futures
from datetime import datetime

from django.core.management.base import BaseCommand
from django.conf import settings

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from sme_ofertaimoveis.imovel.models import Imovel, DemandaImovel


class Command(BaseCommand):
    help = "Cria demanda para os imoveis que não possuem."

    def handle(self, *args, **kwargs):
        print("Criando demandas.")

        total_imoveis = Imovel.objects.filter(excluido=False).count()
        print(f"Total de imóveis: {total_imoveis}")
        imoveis = Imovel.objects.filter(excluido=False).all()[:10]
        import time
        with futures.ThreadPoolExecutor(max_workers=8) as executor:
            to_do = {}
            for ind, imovel in enumerate(imoveis, 1):
                print(f'Imóvel {ind} de {total_imoveis}')
                future = executor.submit(consulta_demanda_imovel, imovel)
                to_do[future] = imovel
                msg = "Agendada para {}: {}"
                print(msg.format(imovel, future))
                time.sleep(0.5)

            for ind, future in enumerate(futures.as_completed(to_do)):
                print(f"Atualizando {ind} de {len(to_do)}")
                results = future.result()

                if results and not isinstance(results, Exception):
                    demanda_imovel = DemandaImovel(imovel=to_do[future])
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
                    print("Demanda Salvar com sucesso!!\n")


def consulta_demanda_imovel(imovel):
    print(f"Começando consulta do imovel: {imovel}")
    
    demanda_imovel = DemandaImovel.objects.filter(imovel=imovel).first()
    if demanda_imovel:
        return

    try:
        url = f'{settings.SCIEDU_URL}/{imovel.latitude}/{imovel.longitude}'
        headers = {
            "Authorization": f'Token {settings.SCIEDU_TOKEN}',
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        results = response.json().get('results')
        print(f"Consulta do imovel: {str(imovel)} terminada.")
    except Exception as e:
        return e

    return results