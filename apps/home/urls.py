# -*- coding: utf-8 -*-
from django.urls import include, path
from rest_framework import routers
from .views import CreateProcedure, ExecuteProcedure
from .api.viewset import (
    TipoProponenteViewSet, BiddersViewSet, BiddersBuildingsViewSet,
    BuildingsContactsViewSet, BiddersBuildingsDocsImagesViewSet
)

router = routers.DefaultRouter()
router.register(
    r'tipo-proponente', TipoProponenteViewSet, basename="tipo-proponente"
)
router.register(
    r'proponentes', BiddersViewSet, basename="proponente"
)
router.register(
    r'imoveis',
    BiddersBuildingsViewSet,
    basename="imoveis"
)
router.register(
    r'contatos',
    BuildingsContactsViewSet,
    basename="imoveis-contatos"
)
router.register(
    r'documentos',
    BiddersBuildingsDocsImagesViewSet,
    basename="imoveis-documentos"
)

urlpatterns = [
    # path('', include(router.urls)),
    path('criasp/', CreateProcedure.as_view(), name='criajustes'),
    path('runsp/', ExecuteProcedure.as_view(), name='rodajustes'),
]