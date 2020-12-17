from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet

from ..serializers import DistritoSerializer
from ...models import Distrito


class DistritoViewset(mixins.ListModelMixin, GenericViewSet):
    pagination_class = None
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = DistritoSerializer
    queryset = Distrito.objects.all()
