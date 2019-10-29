from django.test import TestCase

# Third-party app imports
from model_bakery import baker
from datetime import datetime
from ..models import Imovel, SME_Contatos, Proponente, ContatoImovel


class TestImovel(TestCase):
    def setUp(self):
        self.imovel = baker.make(Imovel, complemento="CASA1", make_m2m=True)

    def test_validade_type_of_fields(self):
        self.assertIsInstance(self.imovel.proponente, Proponente)
        self.assertIsInstance(self.imovel.cep, str)
        self.assertIsInstance(self.imovel.endereco, str)
        self.assertIsInstance(self.imovel.bairro, str)
        self.assertIsInstance(self.imovel.numero, str)
        self.assertIsInstance(self.imovel.complemento, str)
        self.assertIsInstance(self.imovel.latitude, str)
        self.assertIsInstance(self.imovel.longitude, str)
        self.assertIsInstance(self.imovel.criado_em, datetime)

    def test_str(self):
        self.assertEqual(
            str(self.imovel), f"{self.imovel.contato} => {self.imovel.endereco}"
        )


class TestProponente(TestCase):
    def setUp(self):
        self.proponente = baker.make(Proponente, make_m2m=True)

    def test_validade_type_of_fields(self):
        self.assertEqual(self.proponente.nome, None)
        self.assertEqual(self.proponente.cpf_cnpj, "")
        self.assertEqual(self.proponente.email, "")
        self.assertEqual(self.proponente.telefone, "")
        self.assertIsInstance(self.proponente.criado_em, datetime)

    def test_str(self):
        self.assertEqual(
            str(self.proponente),
            f"{self.proponente.nome} => {self.proponente.email} {self.proponente.telefone}",
        )


class TestSME_Contatos(TestCase):
    def setUp(self):
        self.contato = baker.make(SME_Contatos)

    def test_validade_type_of_fields(self):
        self.assertIsInstance(self.contato.nome, str)
        self.assertIsInstance(self.contato.email, str)
        self.assertIsInstance(self.contato.ativo, bool)
        self.assertIsInstance(self.contato.criado_em, datetime)

    def test_str(self):
        self.assertEqual(
            str(self.contato), f"{self.contato.nome} => {self.contato.email}"
        )

    def test_get_contatos_ativos(self):
        self.assertEqual(len(SME_Contatos.objects.get_contatos_ativos()), 1)
        self.contato.ativo = False
        self.contato.save()
        self.assertEqual(len(SME_Contatos.objects.get_contatos_ativos()), 0)


class TestContatoImovel(TestCase):
    def setUp(self):
        self.contato_imovel = baker.make(ContatoImovel)

    def test_validade_type_of_fields(self):
        self.assertIsInstance(self.contato_imovel.nome, str)
        self.assertIsInstance(self.contato_imovel.cpf_cnpj, str)
        self.assertIsInstance(self.contato_imovel.criado_em, datetime)

    def test_str(self):
        self.assertEqual(
            str(self.contato_imovel),
            f"{self.contato_imovel.nome} => {self.contato_imovel.cpf_cnpj}",
        )
