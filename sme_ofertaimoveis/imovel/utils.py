from django.db import connection
from django.db.models import OuterRef, Q, Subquery

from .models import Imovel

def atualiza_imoveis_iptu_duplicado():
    Imovel.objects.filter( 
        numero_iptu__in=Subquery( 
            Imovel.objects.filter(~Q(id=OuterRef('id'))).values('numero_iptu') 
        ),
        situacao__isnull=True
    ).update(situacao='DUPLICACAO_IPTU')

def atualiza_imoveis_endereco_duplicado():
    sql = """
        UPDATE imovel_imovel as i1
           SET situacao = 'DUPLICACAO_ENDERECO'
        FROM imovel_imovel as i2
          WHERE i1.id != i2.id
            AND i1.endereco = i2.endereco
            AND i1.numero = i2.numero
            AND i1.complemento = i2.complemento
            AND i1.bairro = i2.bairro
    """
    with connection.cursor() as cursor:
        cursor.execute(sql)

def checa_digito_verificador_iptu(numero_iptu):
    multiplicacoes = [10, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    soma = 0
    indice = 0
    for digito in [char for char in numero_iptu[:-1] if char.isdigit()]:
        soma += int(digito) * multiplicacoes[indice]
        indice += 1
    mod = soma % 11 if soma % 11 != 10 else 1
    return int(numero_iptu[-1]) == mod
