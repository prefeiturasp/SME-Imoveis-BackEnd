import unittest
from unittest.mock import patch, ANY

from django.test import TestCase

from rest_framework.test import APIClient
from . import DATA_OFERTA_IMOVEL


class TestCadastroImoveisViewSet(TestCase):
    def setUp(self):
        self.api = APIClient()

    @patch("sme_ofertaimoveis.imovel.api.viewsets.task_send_email_to_sme")
    @patch("sme_ofertaimoveis.imovel.api.viewsets.send_email")
    def teste_create_cadastro(self, mk_send_email, mk_task_send_email_to_sme):
        request = self.api.post("/cadastro-imovel/", DATA_OFERTA_IMOVEL, format="json")

        self.assertEqual(request.status_code, 201)

        mk_send_email.assert_called_with(
            subject="Obrigado pelo envio do seu imovel",
            template="email_to_usuario",
            data={},
            to_email="jose@gmail.com",
        )
        mk_task_send_email_to_sme.apply_async.assert_called_with(
            (ANY,), countdown=15
        )
