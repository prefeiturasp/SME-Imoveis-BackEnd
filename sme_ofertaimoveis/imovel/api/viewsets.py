from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins

from .serializers import ImovelSerializer
from ..models import Contato
from ...dados_comuns.utils import send_email


class CadastroImoveisViewSet(ViewSet, mixins.CreateModelMixin):
    permission_classes = (AllowAny,)
    get_serializer = ImovelSerializer
    
    def create(self, request):
    
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        # Envia E-mail SME
        self.send_email_to_sme()

        # Envia E-mail Usuario
        self.send_email_to_usuario(serializer.contato.email)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def send_email_to_sme(self):

        send_email(
            subject="Novo Cadastro de Oferta de Imovel", 
            message_text="Nova oferta de imovel Cadastrada \n"
                         "name: {name}\n"
                         "email: {email}\n"
                         "telephone: {telephone}\n"
                         "cellphone: {cellphone}\n"
                         "address: {address}\n"
                         "neighborhood: {neighborhood}\n"
                         "city: {city}\n"
                         "state: {state}\n"
                         "cep: {cep}\n",
            to_email=email
        )

    def send_email_to_usuario(self, email):

        send_email(
            subject="Obrigado pelo envio do seu imovel", 
            message_text="Em preve vc recebera um contato com a prefeitura", 
            to_email=email
        )
