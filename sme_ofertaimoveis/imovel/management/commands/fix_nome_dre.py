from django.core.management.base import BaseCommand
from sme_ofertaimoveis.dados_comuns.models import DiretoriaRegional

class Command(BaseCommand):
    help = "Atualizar nome da Diretoria Regional de Educação."

    def handle(self, *args, **kwrgs):
        self.stdout.write("Atualizando nomes incorretos...")

        correcoes = [{'id': 12, 'nome': 'FREGUESIA/BRASILÂNDIA'},
                     {'id': 11, 'nome': 'JAÇANÃ/TREMEMBÉ'},
                     {'id': 2, 'nome': 'PIRITUBA/JARAGUÁ'}]

        for data in correcoes:
            dre = DiretoriaRegional.objects.get(id=data['id'])
            dre.nome = data['nome']
            dre.save()

        self.stdout.write("Nomes das Diretorias Regionais atualizados com sucesso!")
