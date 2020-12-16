from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet

from ..serializers import SecretariaSerializer
from ...models import Secretaria


class SecretariaViewset(mixins.ListModelMixin, GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SecretariaSerializer
    queryset = Secretaria.objects.all()
