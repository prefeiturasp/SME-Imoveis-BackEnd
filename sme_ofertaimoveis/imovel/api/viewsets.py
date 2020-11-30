import requests
import json
from django.conf import settings

from rest_framework import status, mixins
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.views import APIView

from .serializers import (
    ImovelSerializer, TipoProponenteSerializer
    # BuscaImovelPeloIPTUSerializer
)
from ..tasks import task_send_email_to_usuario, task_send_email_to_sme
from ..models import TipoProponente, Imovel


class TipoProponenteViewSet(ModelViewSet):
    """
    API endpoint that allows TypeRegisters to be viewed or edited.
    """
    queryset = TipoProponente.objects.all().order_by('nome')
    serializer_class = TipoProponenteSerializer


class CadastroImoveisViewSet(ViewSet, mixins.CreateModelMixin):
    permission_classes = (AllowAny,)
    get_serializer = ImovelSerializer

    def create(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            serializer.save()
            instance = serializer.instance

            # Envia E-mail Usuario

            if instance.proponente and instance.proponente.email:
                task_send_email_to_usuario(
                    instance.proponente.email, protocolo=instance.protocolo
                )

            task_send_email_to_usuario(
                instance.contato.email, protocolo=instance.protocolo
            )

            # Task do E-mail do SES
            task_send_email_to_sme.apply_async((instance.pk,), countdown=15)

            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        except ValidationError as e:
            return Response({'detail': e.args[0]}, status=e.status_code)


class BuscaIPTU(APIView):
    """
    Localiza imóvel pelo número do iptu
    """
    def get(self, request, numero_iptu, format=None):
        queryset = Imovel.objects.filter(
            numero_iptu=numero_iptu
        ).order_by('numero_iptu')
        data = {
            'status': {
                'status_code': 200,
                'status_msgs': 'Ok'
            }
        }
        if queryset:
            data.update({'data': list(queryset.values())})
        else:
            data['status']['status_code'] = 404
            data['status']['status_msgs'] = \
                f'Imóvel com o número de IPTU {numero_iptu} não foi encontrado!'
        return Response(
            data, status=data['status']['status_code']
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