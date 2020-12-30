import logging

import environ
import requests

env = environ.Env()
AUTENTICA_CORESSO_API_TOKEN = env('AUTENTICA_CORESSO_API_TOKEN', default='')
AUTENTICA_CORESSO_API_URL = env('AUTENTICA_CORESSO_API_URL', default='')

LOG = logging.getLogger(__name__)


class AutenticacaoService:
    DEFAULT_HEADERS = {
        "accept": "text/plain",
        'Content-Type': 'application/json',
        'x-api-eol-key': f'{AUTENTICA_CORESSO_API_TOKEN}'
    }
    MULTIPART_DATA_HEADERS = {
        'Content-Type': 'multipart/form-data',
        'x-api-eol-key': f'{AUTENTICA_CORESSO_API_TOKEN}'
    }
    DEFAULT_TIMEOUT = 10

    @classmethod
    def autentica(cls, login, senha):
        payload = {'login': login, 'senha': senha}
        try:
            LOG.info("Autenticando no sme-autentica. Login: %s", login)
            response = requests.post(
                f"{AUTENTICA_CORESSO_API_URL}/v1/autenticacao/",
                headers=cls.DEFAULT_HEADERS,
                timeout=cls.DEFAULT_TIMEOUT,
                json=payload
            )
            return response
        except Exception as e:
            LOG.info("ERROR - %s", str(e))
            raise e

    @classmethod
    def dados(cls, login):
        try:
            LOG.info("Alterando e-amail no sme-autentica. Login: %s", login)
            response = requests.get(
                f"{AUTENTICA_CORESSO_API_URL}/AutenticacaoSgp/{login}/dados/",
                headers=cls.DEFAULT_HEADERS,
                timeout=cls.DEFAULT_TIMEOUT,
            )
            return response
        except Exception as e:
            LOG.info("ERROR - %s", str(e))
            raise e

    @classmethod
    def redefine_email(cls, registro_funcional, email):
        logger.info('Alterando email.')
        try:
            data = {
                'Usuario': registro_funcional,
                'Email': email
            }
            response = requests.post(f'{settings.SME_INTEGRACAO_URL}/api/AutenticacaoSgp/AlterarEmail', data=data,
                                     headers=cls.headers)
            if response.status_code == status.HTTP_200_OK:
                result = "OK"
                return result
            else:
                logger.info("Erro ao redefinir email: %s", response.json())
                raise SmeIntegracaoException('Erro ao redefinir email')
        except Exception as err:
            raise SmeIntegracaoException(str(err))

    @classmethod
    def altera_senha(cls, login, senha):
        data = {'Usuario': login, 'Senha': senha}
        try:
            # LOG.info("Alterando senha no sme-autentica. Login: %s", login)
            response = requests.post(
                f"{AUTENTICA_CORESSO_API_URL}/AutenticacaoSgp/AlterarSenha/",
                headers=cls.MULTIPART_DATA_HEADERS,
                files=data
            )
            print(response.json())
            return response
        except Exception as e:
            LOG.info("ERROR - %s", str(e))
            raise e
