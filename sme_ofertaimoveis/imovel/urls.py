from django.urls import include, path
from rest_framework import routers

from .api.viewsets import CadastroImoveisViewSet

router = routers.DefaultRouter()
router.register("cadastro-imovel", CadastroImoveisViewSet, basename="cadastro-imoveis")

urlpatterns = [path("", include(router.urls))]
