from model_bakery import baker
import pytest

@pytest.fixture
def imovel1():
    return baker.make(
        'Imovel',
        id=1,
        endereco="RUA DOS BOBOS",
        numero=0,
        complemento="CASA1",
        bairro="GARDENS",
        numero_iptu="001"
    )

@pytest.fixture
def imovel2():
    return baker.make(
        'Imovel',
        id=2,
        endereco="RUA DOS BOBOS",
        numero=0,
        complemento="CASA1",
        bairro="GARDENS",
        numero_iptu="002"
    )

@pytest.fixture
def imovel3():
    return baker.make(
        'Imovel',
        id=3,
        endereco="RUA DOS BOBOS",
        numero=0,
        complemento="CASA2",
        bairro="GARDENS",
        numero_iptu="003"
    )

@pytest.fixture
def imovel4():
    return baker.make(
        'Imovel',
        id=4,
        endereco="RUA DOS BOBOS",
        numero=456,
        complemento="CASA1",
        bairro="GARDENS",
        numero_iptu="003"
    )

@pytest.fixture
def imovel5():
    return baker.make(
        'Imovel',
        id=5,
        endereco="RUA DOS BOBOS",
        numero=789,
        complemento="CASA1",
        bairro="GARDENS",
        numero_iptu="003"
    )
