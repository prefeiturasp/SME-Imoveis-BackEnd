from datetime import datetime
from enum import Enum

def checa_digito_verificador_iptu(numero_iptu):
    multiplicacoes = [10, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    soma = 0
    indice = 0
    for digito in [char for char in numero_iptu[:-1] if char.isdigit()]:
        soma += int(digito) * multiplicacoes[indice]
        indice += 1
    mod = soma % 11 if soma % 11 != 10 else 1
    return int(numero_iptu[-1]) == mod

def data_formatada(string_data):
    """Pegar a string isoformat e transformar em uma data no format yyyy-mm-dd"""
    str_d = datetime.strptime(string_data, '%Y-%m-%dT%H:%M:%S.%f').strftime('%Y-%m-%d')
    return datetime.strptime(str_d, '%Y-%m-%d')

class SituacaoDuplicidade(Enum):
    MANTIDO = ''
    DUPLICIDADE_IPTU = "Registro com duplicidade de IPTU."
    DUPLICIDADE_ENDERECO = "Registro com duplicidade de Endereço."
