import base64

from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins

from .serializers import ImovelSerializer
from ...dados_comuns.utils import send_email
from ..tasks import task_send_email_to_sme


class CadastroImoveisViewSet(ViewSet, mixins.CreateModelMixin):
    permission_classes = (AllowAny,)
    get_serializer = ImovelSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        instance = serializer.instance

        # Envia E-mail Usuario
        if instance.proponente.email:
            self.send_email_to_usuario(instance.proponente.email)
        
        self.send_email_to_usuario(instance.contato.email)

        # Task do E-mail do SES
        task_send_email_to_sme.apply_async((instance.pk,), countdown=15)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def send_email_to_usuario(self, email):
        send_email(
            subject="Obrigado pelo envio do seu imovel",
            template="email_to_usuario",
            data={},
            to_email=email,
        )
