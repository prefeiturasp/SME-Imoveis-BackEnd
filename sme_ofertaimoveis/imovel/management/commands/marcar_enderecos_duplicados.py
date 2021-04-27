from django.core.management.base import BaseCommand
from django.db.models import Count, Max

from sme_ofertaimoveis.imovel.models import Imovel
from ...utils import SituacaoDuplicidade


class Command(BaseCommand):
    help = "Identificar o imóveis com endereço duplicado marcando os que devem ser excluídos quando os mesmo já não estão marcados como duplicados por iptu."

    def handle(self, *args, **kwargs):
        self.stdout.write("Marcando imóveis com endereços duplicados.")

        fields = ['endereco', 'bairro', 'numero', 'complemento']
        enderecos_duplicados = (Imovel.objects.values(*fields).order_by().annotate(max_id=Max('id'), count_id=Count('id')).filter(count_id__gt=1))

        for end_dict in enderecos_duplicados.all():
            end_dup = Imovel.objects.filter(**{x: end_dict[x] for x in fields}, excluido=False).order_by('id')
            if end_dup and len(end_dup) > 1:
                self._marca_duplicados(end_dup)
        self.stdout.write("Identificação de endereços duplicados terminada com sucesso.")

    def _marca_duplicados(self, end_dup):
        for ind, ed in enumerate(end_dup):
            if ind != 0:
                ed.excluido = True
            
            if ed.situacao_duplicidade != SituacaoDuplicidade.DUPLICIDADE_IPTU.value:
                ed.situacao_duplicidade = SituacaoDuplicidade.DUPLICIDADE_ENDERECO.value
            ed.save()
            self.stdout.write(f"{ind}, {ed.id}, {ed.bairro}, {ed.numero}, {ed.complemento}, {ed.endereco}, {ed.numero_iptu}, {ed.excluido}, {ed.situacao_duplicidade}") 
            self.stdout.write("")
