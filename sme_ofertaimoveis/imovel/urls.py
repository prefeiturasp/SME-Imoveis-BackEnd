# -*- coding: utf-8 -*-
from django.urls import include, path
from rest_framework import routers

from .api.viewsets import (
    CadastroImoveisViewSet, DemandaRegiao, TipoProponenteViewSet,
    BuscaIPTU
)

router = routers.DefaultRouter()
router.register (
    "tipo-proponente", TipoProponenteViewSet, basename="tipo-proponente"
)
router.register(
    "cadastro-imovel", CadastroImoveisViewSet, basename="cadastro-imoveis"
)

urlpatterns = [
    path("", include(router.urls)),
    path("busca_iptu/<numero_iptu>/", BuscaIPTU.as_view(), name='busca_iptu'),
    path("demanda/<param1>/<param2>/", DemandaRegiao.as_view()),
]
