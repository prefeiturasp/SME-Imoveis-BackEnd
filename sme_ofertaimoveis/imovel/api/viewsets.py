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
from ..models import Imovel, PlantaFoto
from .serializers import CadastroImovelSerializer, AnexoCreateSerializer, AnexoSerializer
from ..tasks import task_send_email_to_usuario, task_send_email_to_sme
from ..utils import checa_digito_verificador_iptu
from django.db.models import Q
from django.db.models import Sum


class CadastroImoveisViewSet(viewsets.ModelViewSet,
                             mixins.CreateModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.ListModelMixin):
    permission_classes = (AllowAny,)
    queryset = Imovel.objects.all()
    get_serializer = CadastroImovelSerializer

    def _filtrar_cadastros(self, request):
        queryset = Imovel.objects.annotate(demandaimovel__total=Sum('demandaimovel__bercario_i') + Sum('demandaimovel__bercario_ii') + Sum('demandaimovel__mini_grupo_i') + Sum('demandaimovel__mini_grupo_ii'))
        if 'protocolo' in request.query_params:
            queryset = queryset.filter(id=request.query_params.get('protocolo'))
        if 'endereco' in request.query_params:
            queryset = queryset.filter(Q(endereco__icontains=request.query_params.get('endereco')))
        if 'area' in request.query_params:
            area = request.query_params.get('area')
            if area == '1':
                queryset = queryset.filter(area_construida__lt=200)
            if area == '2':
                queryset = queryset.filter(area_construida__gte=200, area_construida__lte=500)
            if area == '3':
                queryset = queryset.filter(area_construida__gt=500)
        if 'setor' in request.query_params:
            queryset = queryset.filter(setor__codigo=request.query_params.get('setor'))
        if 'distrito' in request.query_params:
            queryset = queryset.filter(setor__distrito__id=request.query_params.get('distrito'))
        if 'dre' in request.query_params:
            queryset = queryset.filter(setor__distrito__subprefeitura__dre__id=request.query_params.get('dre'))
        if 'status' in request.query_params:
            queryset = queryset.filter(status=request.query_params.get('status'))
        if 'demanda' in request.query_params:
            demanda = request.query_params.get('demanda')
            if demanda == '1':
                queryset = queryset.filter(demandaimovel__total__lt=40)
            if demanda == '2':
                queryset = queryset.filter(demandaimovel__total__gte=40, demandaimovel__total__lte=100)
            if demanda == '3':
                queryset = queryset.filter(demandaimovel__total__gt=100)
        if ('data_inicio' in request.query_params) and ('data_fim' in request.query_params):
            data_inicio = request.query_params.get('data_inicio').split('-')
            data_fim = request.query_params.get('data_fim').split('-')
            dates = [
                        datetime.date(int(data_inicio[0]), int(data_inicio[1]),  int(data_inicio[2])),
                        datetime.date(int(data_fim[0]), int(data_fim[1]),  int(data_fim[2])),
                    ]
            queryset = queryset.filter(criado_em__gte=dates[0], criado_em__lte=dates[1])
        return queryset

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

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        if not request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().update(request, args, kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self._filtrar_cadastros(request)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(
        detail=False,
        methods=['PUT'],
        url_path=f'imoveis/update-status',
        permission_classes=(IsAuthenticated,))
    def update_status(self, request):
        imovel = Imovel.objects.all().get(id=request.query_params.get('id'))
        imovel.situacao = request.query_params.get('situacao')
        imovel.escola = request.query_params.get('escola')
        imovel.codigo_eol = request.query_params.get('codigo_eol')
        imovel.save()
        serializer = self.get_serializer(imovel, context={'request': request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(
        detail=False,
        methods=['GET'],
        url_path=f'imoveis/exportar',
        permission_classes=(IsAuthenticated,))
    def exportar(self, request):
        queryset = self._filtrar_cadastros(request)
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

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


class AnexosViewset(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'
    queryset = PlantaFoto.objects.all()
    serializer_class = AnexoSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return AnexoCreateSerializer
        return AnexoSerializer
