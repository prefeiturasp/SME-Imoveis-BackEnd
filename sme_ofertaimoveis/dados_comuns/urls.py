from django.urls import include, path
from rest_framework import routers

from .api.views import DreViewset, SecretariaViewset, DistritoViewset, SetorViewset 

router = routers.DefaultRouter()
router.register("dres", DreViewset, "Dres")
router.register("secretarias", SecretariaViewset, "Secretarias")
router.register("distritos", DistritoViewset, "Distritos")
router.register("setores", SetorViewset, "Setor")
urlpatterns = [
    path("", include(router.urls)),
]
