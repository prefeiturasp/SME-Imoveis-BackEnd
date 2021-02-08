from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet

from ..serializers.anexo_log_serializer import AnexoLogSerializer
from ...models import LogFluxoStatus, AnexoLog


class AnexoLogViewset(mixins.ListModelMixin,
                      GenericViewSet,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin):
    pagination_class = None
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'uuid'
    serializer_class = AnexoLogSerializer
    queryset = AnexoLog.objects.all()
