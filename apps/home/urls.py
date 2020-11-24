from django.urls import include, path
from rest_framework import routers
from .viewset import (
    TypeRegisterViewSet, BiddersViewSet, BiddersBuildingsViewSet,
    BiddersBuildingsContactsViewSet, BiddersBuildingsDocsImagesViewSet
)

router_imoveis = routers.DefaultRouter()
router_imoveis.register(
    r'tipo_cadastrante', TypeRegisterViewSet, basename="tipo-proponente"
)
router_imoveis.register(
    r'proponentes', BiddersViewSet, basename="proponente"
)
router_imoveis.register(
    r'proponentes/<str: pk>',
    BiddersViewSet,
    basename="consulta-proponente"
)
router_imoveis.register(
    r'imoveis/<str: pk>',
    BiddersBuildingsViewSet,
    basename="imoveis"
)
router_imoveis.register(
    r'contatos/<str: pk>',
    BiddersBuildingsContactsViewSet,
    basename="imoveis-contatos"
)
router_imoveis.register(
    r'documentos/<str: pk>',
    BiddersBuildingsDocsImagesViewSet,
    basename="imoveis-documentos"
)

urlpatterns = [
    path('', include(router_imoveis.urls)),
]