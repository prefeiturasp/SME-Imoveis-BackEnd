# -*- coding: utf-8 -*-
from django.urls import include, path
from rest_framework import routers
from .api.viewset import (
    TypeRegisterViewSet, BiddersViewSet, BiddersBuildingsViewSet,
    BiddersBuildingsContactsViewSet, BiddersBuildingsDocsImagesViewSet
)

router = routers.DefaultRouter()
router.register(
    r'tipo_cadastrante', TypeRegisterViewSet, basename="tipo-proponente"
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
    BiddersBuildingsContactsViewSet,
    basename="imoveis-contatos"
)
router.register(
    r'documentos',
    BiddersBuildingsDocsImagesViewSet,
    basename="imoveis-documentos"
)

urlpatterns = [
    path('', include(router.urls)),
]