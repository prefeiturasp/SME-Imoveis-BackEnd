import json
import logging

import requests
from django.conf import settings
from rest_framework import status

logger = logging.getLogger(__name__)


class SmeIntegracaoException(Exception):
    pass


class SmeIntegracaoService:
    headers = {
        'accept': 'application/json',
        'x-api-eol-key': f'{settings.SME_INTEGRACAO_TOKEN}'
    }
    timeout = 20

    @classmethod
    def redefine_senha(cls, registro_funcional, senha):
        """Se a nova senha for uma das senhas padões, a API do SME INTEGRAÇÃO
        não deixa fazer a atualização.
        Para resetar para a senha padrão é preciso usar o endpoint ReiniciarSenha da API SME INTEGRAÇÃO"""
        logger.info('Alterando senha.')
        try:
            data = {
                'Usuario': registro_funcional,
                'Senha': senha
            }
            response = requests.post(f'{settings.SME_INTEGRACAO_URL}/api/AutenticacaoSgp/AlterarSenha', data=data, headers=cls.headers)
            return response
        except Exception as err:
            raise SmeIntegracaoException(str(err))

    @classmethod
    def redefine_email(cls, registro_funcional, email):
        logger.info('Alterando email.')
        try:
            data = {
                'Usuario': registro_funcional,
                'Email': email
            }
            response = requests.post(f'{settings.SME_INTEGRACAO_URL}/api/AutenticacaoSgp/AlterarEmail', data=data, headers=cls.headers)
            return response
        except Exception as err:
            raise SmeIntegracaoException(str(err))

    
    @classmethod
    def informacao_usuario_sgp(cls, login):
        logger.info('Consultando informação de %s.', login)
        try:
            response = requests.get(f'{settings.SME_INTEGRACAO_URL}/api/AutenticacaoSgp/{login}/dados', headers=cls.headers)
            if response.status_code == status.HTTP_200_OK:
                return response.json()
            else:
                logger.info("Dados não encontrados: %s", response)
                raise SmeIntegracaoException('Dados não encontrados.')
        except Exception as err:
            logger.info("Erro ao consultar informação: %s", str(err))
            raise SmeIntegracaoException(str(err))
