from django.core.exceptions import ObjectDoesNotExist, ValidationError as coreValidationError
from django.db.models import Q
from rest_framework import status, permissions, mixins
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.views import ObtainJSONWebToken

from .serializers import UserSerializer, PerfilSerializer
from .services import AutenticacaoService
from ..models import Perfil, User
from ...dados_comuns.models import Setor, Secretaria


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.request.user.id)

    def _get_usuario_por_rf(self, registro_funcional):
        return User.objects.get(username=registro_funcional)

    # TODO: colocar lógica no serializer; verificar porque só deixa dar update no usuário logado
    def update(self, request, *args, **kwargs):
        username = kwargs.get('username')
        usuario = User.objects.get(username=username)
        if request.data.get('secretaria_'):
            usuario.secretaria = Secretaria.objects.get(id=request.data.get('secretaria_'))
        else:
            usuario.secretaria = None
        if request.data.get('setor'):
            try:
                setor_ = Setor.objects.get(codigo=request.data.get('setor').get('codigo'))
                usuario.setor = setor_
            except ObjectDoesNotExist:
                return Response({"detail": "Setor não existe"}, status=status.HTTP_400_BAD_REQUEST)
        if 'perfil_' in request.data:
            if request.data.get('perfil_') == 'SEM PERMISSAO':
                usuario.perfil = None
            else:
                perfil = Perfil.objects.get(id=request.data.get('perfil_'))
                if perfil.nome == 'ADMIN' and User.objects.filter(perfil__nome='ADMIN').count() == 3:
                    return Response({"detail": "Excedeu o limite de usuários ADMIN no sistema"},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif perfil.nome == 'SECRETARIA' and User.objects.filter(perfil__nome='SECRETARIA').count() == 3:
                    return Response({"detail": "Excedeu o limite de usuários SECRETARIA no sistema"},
                                    status=status.HTTP_400_BAD_REQUEST)
                usuario.perfil = Perfil.objects.get(id=request.data.get('perfil_'))
        usuario.save()
        serializer = UserSerializer(usuario)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = User.objects.all()
        if 'secretaria' in request.query_params:
            queryset = queryset.filter(secretaria=request.query_params.get('secretaria'))
        if 'dre' in request.query_params:
            queryset = queryset.filter(setor__distrito__subprefeitura__dre=request.query_params.get('dre'))
        if 'perfil' in request.query_params:
            if request.query_params.get('perfil') == 'SEM PERMISSAO':
                queryset = queryset.filter(perfil__isnull=True)
            else:
                queryset = queryset.filter(perfil=request.query_params.get('perfil'))
        if 'nome' in request.query_params:
            queryset = queryset.filter(Q(first_name__icontains=request.query_params.get('nome')) |
                                       Q(last_name__icontains=request.query_params.get('nome')))
        serializer = UserSerializer(queryset, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

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
