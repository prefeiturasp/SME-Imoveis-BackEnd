from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from ..serializers import DistritoSerializer
from ...models import Distrito, Subprefeitura


class DistritoViewset(mixins.ListModelMixin, GenericViewSet):
    pagination_class = None
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = DistritoSerializer
    queryset = Distrito.objects.all()

    @action(
        detail=False,
        methods=['GET'],
        url_path=f'get_distritos_por_dre',
        permission_classes=(IsAuthenticated,))
    def get_distritos_por_dre(self, request):
        subprefeituras = Subprefeitura.objects.filter(dre__id__in=request.query_params.getlist('dre'))
        subprefeituras_ids = []
        for subprefeitura in subprefeituras:
            subprefeituras_ids.append(subprefeitura.id)

        queryset = Distrito.objects.filter(subprefeitura__id__in=subprefeituras_ids)

        serializer = self.get_serializer(queryset, many=True)
        return Response(
            data=serializer.data, status=status.HTTP_200_OK
        )
