from django.urls import include, path
from rest_framework import routers

from .api.views import DreViewset, SecretariaViewset

router = routers.DefaultRouter()
router.register("dres", DreViewset, "Dres")
router.register("secretarias", SecretariaViewset, "Secretarias")

urlpatterns = [
    path("", include(router.urls)),
]
