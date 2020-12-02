# -*- coding: utf-8 -*-
from django.urls import include, path
# from rest_framework import routers
from .views import CreateProcedure, ExecuteProcedure
# from .api.viewset import (
#     TipoProponenteViewSet, BiddersViewSet, BiddersBuildingsViewSet,
#     BiddersBuildingsDocsImagesViewSet
# )

# router = routers.DefaultRouter()
# router.register(
#     r'home_tipo_proponente', TipoProponenteViewSet, basename="home_tipo_proponente"
# )
# router.register(
#     r'home_proponentes', BiddersViewSet, basename="home_proponentes"
# )
# router.register(
#     r'home_imoveis',
#     BiddersBuildingsViewSet,
#     basename="home_imoveis"
# )
# router.register(
#     r'home_documentos',
#     BiddersBuildingsDocsImagesViewSet,
#     basename="home_imoveis_documentos"
# )

urlpatterns = [
    # path('', include(router.urls)),
    path('criasp/', CreateProcedure.as_view(), name='criajustes'),
    path('runsp/', ExecuteProcedure.as_view(), name='rodajustes'),
]