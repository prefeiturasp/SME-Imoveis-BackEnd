import unittest
from django.test import TestCase

# Third-party app imports
from model_bakery import baker
from ..models import Imovel, Proponente, ContatoImovel
from ..api.serializers import (
    ContatoSerializer,
    ProponenteSerializer,
    EnderecoSerializer,
    ImovelSerializer,
)
from . import DATA_OFERTA_IMOVEL


class TestImovelSerializer(TestCase):
    def setUp(self):
        self.imovel = baker.make(Imovel, complemento="CASA1", make_m2m=True)

    def test_serializer(self):

        serializer = ImovelSerializer(self.imovel)
        self.assertIsInstance(serializer.data, dict)

    def test_create(self):
        news_obj = ImovelSerializer(data=DATA_OFERTA_IMOVEL)

        self.assertTrue(news_obj.is_valid())
        news_obj.save()
        self.assertNotEqual(self.imovel.pk, news_obj.instance.pk)


class TestContatoImoveSerializerl(TestCase):
    def setUp(self):
        self.contato = baker.make(ContatoImovel)

    def test_serializer(self):

        serializer = ContatoSerializer(self.contato)
        self.assertIsInstance(serializer.data, dict)


class TestProponenteSerializer(TestCase):
    def setUp(self):
        self.proponente = baker.make(Proponente)

    def test_serializer(self):

        serializer = ProponenteSerializer(self.proponente)
        self.assertIsInstance(serializer.data, dict)


class TestEnderecoSerializer(TestCase):
    def setUp(self):
        self.imovel = baker.make(Imovel, complemento="CASA1", make_m2m=True)

    def test_serializer(self):

        serializer = EnderecoSerializer(self.imovel)
        self.assertIsInstance(serializer.data, dict)
