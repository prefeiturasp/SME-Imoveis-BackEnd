from django.urls import include, path
from rest_framework import routers
from .viewset import SMEContactsViewSet, TypeRegisterViewSet, RegisterViewSet

router_imoveis = routers.DefaultRouter()
router_imoveis.register(r'sme_contatos', SMEContactsViewSet)
router_imoveis.register(r'tipo_cadastrante', TypeRegisterViewSet)
router_imoveis.register(r'cadastrantes', RegisterViewSet)

urlpatterns = [
    path('', include(router_imoveis.urls)),
]