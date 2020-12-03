import requests

from django.conf import settings

from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView

from .serializers import ImovelSerializer
from ..models import Imovel
from ..tasks import task_send_email_to_usuario, task_send_email_to_sme
from ..utils import checa_digito_verificador_iptu


class CadastroImoveisViewSet(ViewSet, mixins.CreateModelMixin):
    permission_classes = (AllowAny,)
    get_serializer = ImovelSerializer

    def create(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            serializer.save()
            instance = serializer.instance
            """
            # Envia E-mail Usuario

            if instance.proponente and instance.proponente.email:
                task_send_email_to_usuario(instance.proponente.email, protocolo=instance.protocolo)

            task_send_email_to_usuario(instance.contato.email, protocolo=instance.protocolo)

            # Task do E-mail do SES
            task_send_email_to_sme.apply_async((instance.pk,), countdown=15)
            """
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        except ValidationError as e:
            return Response({'detail': e.args[0]}, status=e.status_code)

    @action(detail=False,
            methods=['get'],
            url_path='checa-iptu-ja-existe/(?P<numero_iptu>.*)')
    def checa_iptu_ja_existe(self, request, numero_iptu=None):
        iptu_existe = numero_iptu in Imovel.objects.all().values_list('numero_iptu', flat=True)
        iptu_valido = checa_digito_verificador_iptu(numero_iptu)
        return Response(
            {'iptu_existe': iptu_existe, 'iptu_valido': iptu_valido}, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['post'], url_path='checa-endereco-imovel-ja-existe')
    def checa_endereco_imovel_ja_existe(self, request):
        endereco_existe = Imovel.objects.filter(
            cep=request.data.get('cep'),
            endereco=request.data.get('endereco'),
            bairro=request.data.get('bairro'),
            numero=request.data.get('numero')
        ).exists()
        return Response(
            {'endereco_existe': endereco_existe}, status=status.HTTP_200_OK
        )


class DemandaRegiao(APIView):
    """
    Encapsula a chamada a API de demanda
    """
    permission_classes = (AllowAny,)

    def get(self, request, param1, param2, format=None):
        url = f'{settings.SCIEDU_URL}/{param1}/{param2}'
        headers = {
            "Authorization": f'Token {settings.SCIEDU_TOKEN}',
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        return Response(response.json(), status=response.status_code)
