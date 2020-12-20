import datetime
import requests

from django.conf import settings

from rest_framework import status, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from ..models import Imovel
from .serializers import CadastroImovelSerializer
from ..tasks import task_send_email_to_usuario, task_send_email_to_sme
from ..utils import checa_digito_verificador_iptu


class CadastroImoveisViewSet(viewsets.ModelViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    permission_classes = (AllowAny,)
    queryset = Imovel.objects.all()
    get_serializer = CadastroImovelSerializer

    def _agrupa_por_mes_por_solicitacao(self, query_set: list) -> dict:
        # TODO: melhorar performance
        sumario = {'novos_cadastros': 0, 'proximos_ao_vencimento': 0, 'atrasados': 0}  # type: dict
        _25_dias_atras = datetime.date.today() - datetime.timedelta(days=25)
        _30_dias_atras = datetime.date.today() - datetime.timedelta(days=30)
        sumario['novos_cadastros'] = query_set.filter(criado_em__gte=_25_dias_atras).count()
        sumario['proximos_ao_vencimento'] = query_set.filter(criado_em__lt=_25_dias_atras,
                                                             criado_em__gte=_30_dias_atras).count()
        sumario['atrasados'] = query_set.filter(criado_em__lt=_30_dias_atras).count()
        return sumario

    @action(
        detail=False,
        methods=['GET'],
        url_path=f'ultimos-30-dias',
        permission_classes=(IsAuthenticated,))
    def ultimos_30_dias(self, request):
        query_set = Imovel.objects.filter(criado_em__gt=datetime.date.today() - datetime.timedelta(days=30))
        resumo_do_mes = self._agrupa_por_mes_por_solicitacao(query_set=query_set)
        return Response(resumo_do_mes, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['GET'],
        url_path=f'imoveis/novos-cadastros',
        permission_classes=(IsAuthenticated,))
    def imoveis_novos_cadastros(self, request):
        query_set = Imovel.objects.filter(criado_em__gt=datetime.date.today() - datetime.timedelta(days=25))
        page = self.paginate_queryset(query_set)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(
        detail=False,
        methods=['GET'],
        url_path=f'imoveis/proximos-ao-vencimento',
        permission_classes=(IsAuthenticated,))
    def imoveis_proximos_ao_vencimento(self, request):
        _25_dias_atras = datetime.date.today() - datetime.timedelta(days=25)
        _30_dias_atras = datetime.date.today() - datetime.timedelta(days=30)
        query_set = Imovel.objects.filter(criado_em__lt=_25_dias_atras,
                                          criado_em__gte=_30_dias_atras)
        page = self.paginate_queryset(query_set)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(
        detail=False,
        methods=['GET'],
        url_path=f'imoveis/atrasados',
        permission_classes=(IsAuthenticated,))
    def imoveis_atrasados(self, request):
        _30_dias_atras = datetime.date.today() - datetime.timedelta(days=30)
        query_set = Imovel.objects.filter(criado_em__lt=_30_dias_atras)
        page = self.paginate_queryset(query_set)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

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
