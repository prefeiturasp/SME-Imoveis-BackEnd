from django.core.management.base import BaseCommand
from django.db.models import Count

from sme_ofertaimoveis.imovel.models import Imovel

from enum import Enum

from ...utils import SituacaoDuplicidade

class Command(BaseCommand):
    help = "Identificar o imóveis com iptu duplicado marcando os que devem ser excluídos e o que vai ser válido."

    def handle(self, *args, **kwargs):
        self.stdout.write("Marcando imóveis com iptus duplicados.")

        iptus_duplicados = Imovel.objects.values('numero_iptu').annotate(mycount=Count('numero_iptu')).values('numero_iptu').order_by().filter(mycount__gt=1)
        for iptu_dict in iptus_duplicados.all():
           self.stdout.write(iptu_dict['numero_iptu'])
           if iptu_dict['numero_iptu']:
               self._marca_duplicados(iptu_dict['numero_iptu'])
        self.stdout.write("Identificação de iptus duplicados terminada com sucesso.")

    def _marca_duplicados(self, iptu):
        duplicados = Imovel.objects.filter(numero_iptu=iptu).order_by('id')
        for ind, duplicado in enumerate(duplicados):
            self.stdout.write(f"{ind}, {duplicado.id}, {duplicado.protocolo}, {duplicado.numero_iptu}")
            if ind != 0:
                duplicado.excluido = True
                self.stdout.write(f"Imóvel com protocolo {duplicado.protocolo} será MARCADO para excluído.")

            duplicado.situacao_duplicidade = SituacaoDuplicidade.DUPLICIDADE_IPTU.value
            duplicado.save()
