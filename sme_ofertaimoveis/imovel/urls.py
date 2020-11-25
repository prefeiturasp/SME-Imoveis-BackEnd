# -*- coding: utf-8 -*-
from django.urls import include, path
from rest_framework import routers

from .api.viewsets import CadastroImoveisViewSet, DemandaRegiao

router = routers.DefaultRouter()
router.register("cadastro-imovel", CadastroImoveisViewSet, basename="cadastro-imoveis")

urlpatterns = [
    path("", include(router.urls)),
    path("demanda/<param1>/<param2>/", DemandaRegiao.as_view())
]
