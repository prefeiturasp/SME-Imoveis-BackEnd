from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins

from .serializers import ImovelSerializer
from ..tasks import task_send_email_to_usuario, task_send_email_to_sme


class CadastroImoveisViewSet(ViewSet, mixins.CreateModelMixin):
    permission_classes = (AllowAny,)
    get_serializer = ImovelSerializer

    def create(self, request):
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
