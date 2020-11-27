import requests

from django.conf import settings

from rest_framework import status, mixins
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.views import APIView

from .serializers import ImovelSerializer, TipoProponenteSerializer
from ..tasks import task_send_email_to_usuario, task_send_email_to_sme
from ..models import TipoProponente


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
                task_send_email_to_usuario(instance.proponente.email, protocolo=instance.protocolo)

            task_send_email_to_usuario(instance.contato.email, protocolo=instance.protocolo)

            # Task do E-mail do SES
            task_send_email_to_sme.apply_async((instance.pk,), countdown=15)

            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        except ValidationError as e:
            return Response({'detail': e.args[0]}, status=e.status_code)


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