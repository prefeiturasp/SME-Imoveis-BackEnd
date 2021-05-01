from django.core.management.base import BaseCommand
from sme_ofertaimoveis.imovel.models import Imovel, Setor

import requests


class Command(BaseCommand):
    help = "Atualiza setor de imóveis não marcados para serem excluídos"

    def handle(self, *args, **kwargs):
        self.stdout.write("Atualizando setores dos imóveis.")
        url_localizador = "https://escolaaberta.sme.prefeitura.sp.gov.br/api/localizador?lat={0}&lon={1}&radius=100"
        imoveis = Imovel.objects.filter(excluido=False).all()
        print(f"Total de imóveis {len(imoveis)}")
        for imovel in imoveis:
            try:
                response = requests.get(url_localizador.format(imovel.latitude, imovel.longitude))
                result = response.json()
                codigo_setor = result['results'][0]['setor']
                setor = Setor.objects.filter(codigo=f"{codigo_setor}".zfill(4)).first()
                
                if not setor:
                    print(f"Setor com código {'codigo'.zfill(4)} não econtrado.")
                    continue

                imovel.setor = setor
                imovel.save()
                print("setor", setor)
            except Exception as e:
                print("Erro ao atualizar setor: %s, imóvel: %s", str(e), str(imovel))

        self.stdout.write("Atualização finalizada com sucesso.")
