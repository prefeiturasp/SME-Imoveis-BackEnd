from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, ValidationError as coreValidationError
from rest_framework import status, permissions, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.views import ObtainJSONWebToken

from .serializers import UserSerializer, PerfilSerializer
from .services import AutenticacaoService
from ..models import Perfil

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


class PerfilViewset(mixins.ListModelMixin, GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PerfilSerializer
    queryset = Perfil.objects.all()


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


class LoginView(ObtainJSONWebToken):
    """
    POST auth/login/
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        login = request.data.get("login", "")
        senha = request.data.get("senha", "")
        try:
            response = AutenticacaoService.autentica(login, senha)
            if response.status_code == 200:
                user_dict = response.json()
                if 'usuarioId' in user_dict.keys():
                    try:
                        user = User.objects.get(username=login)
                        user.first_name = user_dict['nome'].split(' ')[0]
                        user.last_name = ' '.join(user_dict['nome'].split(' ')[1:])
                        user.set_password(senha)
                        user.save()
                    except User.DoesNotExist:
                        # logger.info("Usuário %s não encontrado.", login)
                        # return Response({'data': {'detail': 'Usuário não encontrado.'}}, status=status.HTTP_401_UNAUTHORIZED)
                        user = User()
                        user.username = login
                        user.first_name = user_dict['nome'].split(' ')[0]
                        user.last_name = ' '.join(user_dict['nome'].split(' ')[1:])
                        user.set_password(senha)
                        user.save()
                    request._full_data = {'username': login, 'password': senha}
                    resp = super().post(request, *args, **kwargs)
                    user_dict['permissoes'] = self.get_user_permissions(user)
                    data = {**user_dict, **resp.data}
                    return Response(data)
            return Response(response.json(), response.status_code)
        except Exception as e:
            return Response({'data': {'detail': f'ERROR - {e}'}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_user_permissions(self, user):
        perms = []
        for group in user.groups.all():
            for permission in group.permissions.all():
                perms.append(permission.codename)

        return perms