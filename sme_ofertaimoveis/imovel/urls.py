from django.urls import include, path
from rest_framework import routers

from .api.viewsets import CadastroImoveisViewSet, DemandaRegiao, AnexosViewset

router = routers.DefaultRouter()
router.register("cadastro-imovel", CadastroImoveisViewSet, basename="cadastro-imoveis")
router.register("plantafoto", AnexosViewset, basename="planta-foto")

urlpatterns = [
    path("", include(router.urls)),
    path("demanda/<param1>/<param2>/", DemandaRegiao.as_view())
]
