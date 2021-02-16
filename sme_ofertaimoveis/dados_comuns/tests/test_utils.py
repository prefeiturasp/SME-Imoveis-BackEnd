import unittest
from unittest.mock import patch, ANY, MagicMock

from django.conf import settings
from django.test import TestCase

from ..utils import send_email, consult_api_fila_creche, TerceirizadasClient


class TestSendEmail(TestCase):
    @patch("sme_ofertaimoveis.dados_comuns.utils.render_to_string")
    @patch("sme_ofertaimoveis.dados_comuns.utils.EmailMessage")
    def test_send_email_call(self, mk_EmailMessage, mk_render_to_string):
        experienced = {
            "subject": "Obrigado pelo envio do seu imovel",
            "template": "email_to_usuario",
            "data": {},
            "to_email": "maria@gmail.com",
        }

        mk_render_to_string.side_effect = ["msg_plain", "msg_html"]

        send_email(**experienced)
        mk_EmailMessage.assert_called_with(
            subject=experienced["subject"],
            body="msg_plain",
            from_email=ANY,
            bcc=[experienced["to_email"]],
        )


class TestConsultApiFilaCreche(TestCase):
    @patch("sme_ofertaimoveis.dados_comuns.utils.requests")
    def test_consult_api(self, mk_request):

        consult_api_fila_creche("123456", "654321", "1")
        mk_request.request.assert_called_with(
            "GET",
            f"{settings.FILA_CRECHE_URL}/api/v1/schools/radius/wait/654321/123456/1",
            headers={"Content-Type": "application/json"},
        )

    @patch("sme_ofertaimoveis.dados_comuns.utils.requests")
    def test_consult_api_return_data(self, mk_request):

        mk_response = MagicMock()
        mk_response.json.return_value = {"results": "OK"}
        mk_request.request.return_value = mk_response

        retorno = consult_api_fila_creche("123456", "654321", "1")
        self.assertEqual(retorno, "OK")


class TestTerceirizadasClient(TestCase):
    @patch("sme_ofertaimoveis.dados_comuns.utils.requests")
    def test_consulta_dres(self, mk_request):

        TerceirizadasClient.dres()
        mk_request.get.assert_called_with(
            f"{TerceirizadasClient.url}/dres",
            headers=TerceirizadasClient.headers,
        )

    @patch("sme_ofertaimoveis.dados_comuns.utils.requests")
    def test_consulta_subprefeituras(self, mk_request):

        TerceirizadasClient.subprefeituras()
        mk_request.get.assert_called_with(
            f"{TerceirizadasClient.url}/subprefeituras",
            headers=TerceirizadasClient.headers,
        )
    
    @patch("sme_ofertaimoveis.dados_comuns.utils.requests")
    def test_consulta_distritos(self, mk_request):

        TerceirizadasClient.distritos()
        mk_request.get.assert_called_with(
            f"{TerceirizadasClient.url}/distritos",
            headers=TerceirizadasClient.headers,
        )
    
    @patch("sme_ofertaimoveis.dados_comuns.utils.requests")
    def test_consulta_setores(self, mk_request):

        TerceirizadasClient.setores()
        mk_request.get.assert_called_with(
            f"{TerceirizadasClient.url}/setores",
            headers=TerceirizadasClient.headers,
        )
