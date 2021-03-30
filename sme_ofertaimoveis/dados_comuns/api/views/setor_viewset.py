from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from ..serializers import SetorSerializer
from ...models import Setor


class SetorViewset(mixins.ListModelMixin, GenericViewSet):
    pagination_class = None
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SetorSerializer
    queryset = Setor.objects.all()

    @action(
        detail=False,
        methods=['GET'],
        url_path=f'get_setores_por_distrito',
        permission_classes=(IsAuthenticated,))
    def get_setores_por_distrito(self, request):
        queryset = Setor.objects.filter(distrito__id__in=request.query_params.getlist('distrito'))
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            data=serializer.data, status=status.HTTP_200_OK
        )
