from django.urls import include, path
from rest_framework import routers

from .api import viewsets

router = routers.DefaultRouter()

router.register('usuarios', viewsets.UserViewSet, 'Usuários')
router.register('confirmar_email/(?P<uuid>[^/]+)/(?P<confirmation_key>[^/]+)',
                viewsets.UsuarioConfirmaEmailViewSet, 'Confirmar E-mail')
router.register('perfis', viewsets.PerfilViewset, 'Perfis')

urlpatterns = [
    path('', include(router.urls))
]