from django.core.management.base import BaseCommand
from sme_ofertaimoveis.imovel.models import Imovel, Proponente
from openpyxl import Workbook, load_workbook
from openpyxl.writer.excel import save_virtual_workbook
from sme_ofertaimoveis.users.models import User
from django.db import connection
import datetime

class Command(BaseCommand):
    help = "Atualizar campo proprietário dos imóveis cadastrados com base na planilha."

    def handle(self, *args, **kwrgs):
        self.stdout.write("Atualizando planilha.")
        # Trocar para nome da planilha correto
        self.autalizar_planilha('Protocolos_Sistema Cadastro de Imóveis 12-05-2021.xlsx')
        self.stdout.write("Processo de atualização finalizado.")

    def autalizar_planilha(self, nome_arquivo):
        wb = load_workbook(filename = nome_arquivo)
        # Trocar para sheet correto
        sheet_ranges = wb['Relatório por Status']
        linhas = sheet_ranges.max_row
        colunas = sheet_ranges.max_column
        cursor = connection.cursor()

        for i in range(2, linhas + 1):
            protocolo = sheet_ranges.cell(row=i, column=3).value
            raw_query = f"SELECT nome FROM imovel_contatoimovel WHERE id={protocolo}"
            cursor.execute(raw_query)
            nome = cursor.fetchall()[0][0]
            sheet_ranges.cell(row=i, column=11, value=nome)
        wb.save("Protocolos_Sistema Cadastro de Imóveis 12-05-2021.xlsx")
