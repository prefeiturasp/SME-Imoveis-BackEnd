from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet

from ..serializers import DreSerializer
from ...models import DiretoriaRegional


class DreViewset(mixins.ListModelMixin, GenericViewSet):
    pagination_class = None
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = DreSerializer
    queryset = DiretoriaRegional.objects.all()
