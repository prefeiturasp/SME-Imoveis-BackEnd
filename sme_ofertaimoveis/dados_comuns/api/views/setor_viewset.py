from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet

from ..serializers import SetorSerializer
from ...models import Setor


class SetorViewset(mixins.ListModelMixin, GenericViewSet):
    pagination_class = None
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SetorSerializer
    queryset = Setor.objects.all()
