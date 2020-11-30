# -*- coding: utf-8 -*-
import environ
from des import urls as des_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from sme_ofertaimoveis.imovel.urls import router

env = environ.Env()

schema_view = get_schema_view(
    openapi.Info(
        title="API de Oferta Imoveis",
        default_version='v1',
        description="API para manutenção do cadastro de imóvies SME",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # path('swagger/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('docs/', schema_view.with_ui('docs', cache_timeout=0), name='schema-redoc'),
    path("docs/", schema_view.with_ui('redoc'), name="schema-redoc"),
    path("django-des/", include(des_urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("admin/", admin.site.urls),
    path("api-token-auth/", obtain_jwt_token),
    path("api-token-refresh/", refresh_jwt_token),
    path('', include('apps.home.urls')),
    path('', include('sme_ofertaimoveis.imovel.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ADDING ROUTERS FROM ALL APPS
# urlpatterns += router.urls
