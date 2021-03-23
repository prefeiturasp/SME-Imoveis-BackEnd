from django.core.management.base import BaseCommand
from sme_ofertaimoveis.imovel.models import Imovel


class Command(BaseCommand):
    help = "Normaliza o iptu dos imíveis retirando: ',', '.', '-', '/' e espaços em branco."

    def handle(self, *args, **kwrgs):
        self.stdout.write("Normalizando os iptus dos imóveis.")

        # Textos não foram retirados dos campos de iptu.
        for i in Imovel.objects.all():
            self.stdout.write(f"{i.numero_iptu}, {i.numero_iptu.replace('.', '').replace('-', '').replace('/', '').replace(' ', '')}")
            i.numero_iptu = i.numero_iptu.replace('.', '').replace('-', '').replace('/', '').replace(" ", "")
            i.save()
        self.stdout.write("Processo de ajuste de iptus finalizado.")
