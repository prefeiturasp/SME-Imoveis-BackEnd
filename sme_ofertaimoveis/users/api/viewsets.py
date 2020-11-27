from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, ValidationError as coreValidationError
from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.request.user.id)

    def _get_usuario_por_rf(self, registro_funcional):
        return User.objects.get(username=registro_funcional)

    def create(self, request):  # noqa C901
        try:
            assert not User.objects.filter(
                username=request.data.get('username')
            ).exists(), 'Usuário existente no sistema'
            usuario = UserSerializer().create(request.data)
            usuario.enviar_email_confirmacao()
            return Response(UserSerializer(usuario).data)
        except ValidationError as e:
            return Response({'detail': e.detail[0].title()}, status=status.HTTP_400_BAD_REQUEST)
        except AssertionError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["GET"], permission_classes=(IsAuthenticated,))
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=False, url_path='recuperar-senha/(?P<registro_funcional>.*)')
    def recuperar_senha(self, request, registro_funcional=None):
        try:
            usuario = self._get_usuario_por_rf(registro_funcional)
        except ObjectDoesNotExist:
            return Response({'detail': 'Não existe usuário com este e-mail ou RF'},
                            status=status.HTTP_400_BAD_REQUEST)
        usuario.enviar_email_recuperacao_senha()
        return Response({'email': f'{usuario.email}'})

    @action(detail=False, methods=['POST'], url_path='atualizar-senha/(?P<usuario_uuid>.*)/(?P<token_reset>.*)')  # noqa
    def atualizar_senha(self, request, usuario_uuid=None, token_reset=None):
        # TODO: melhorar este método
        senha1 = request.data.get('senha1')
        senha2 = request.data.get('senha2')
        if senha1 != senha2:
            return Response({'detail': 'Senhas divergem'}, status.HTTP_400_BAD_REQUEST)
        try:
            usuario = User.objects.get(uuid=usuario_uuid)
        except ObjectDoesNotExist:
            return Response({'detail': 'Não existe usuário com este e-mail ou RF'},
                            status=status.HTTP_400_BAD_REQUEST)
        if usuario.atualiza_senha(senha=senha1, token=token_reset):

            return Response({'sucesso!': 'senha atualizada com sucesso'})
        else:
            return Response({'detail': 'Token inválido'}, status.HTTP_400_BAD_REQUEST)


class UsuarioConfirmaEmailViewSet(GenericViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def list(self, request, uuid, confirmation_key):  # noqa C901
        try:
            usuario = User.objects.get(uuid=uuid)
            usuario.confirm_email(confirmation_key)
            usuario.is_active = usuario.is_confirmed
            usuario.save()
        except ObjectDoesNotExist:
            return Response({'detail': 'Erro ao confirmar email'},
                            status=status.HTTP_400_BAD_REQUEST)
        except coreValidationError:
            return Response({'detail': 'Parâmetros para confirmação de e-mail inválidos'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(UserSerializer(usuario).data)
