import pytest
from sme_ofertaimoveis.imovel.models import Imovel
from sme_ofertaimoveis.imovel.utils import (
    atualiza_imoveis_endereco_duplicado,
    atualiza_imoveis_iptu_duplicado
)

@pytest.mark.django_db
def test_atualiza_imoveis_iptu_duplicado(imovel1, imovel2, imovel3, imovel4, imovel5):
    atualiza_imoveis_iptu_duplicado()
    assert Imovel.objects.filter(situacao='DUPLICACAO_IPTU').count() == 3

@pytest.mark.django_db
def test_atualiza_imoveis_endereco_duplicado(imovel1, imovel2, imovel3, imovel4, imovel5):
    atualiza_imoveis_endereco_duplicado()
    assert Imovel.objects.filter(situacao='DUPLICACAO_ENDERECO').count() == 2