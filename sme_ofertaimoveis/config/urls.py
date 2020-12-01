import environ
from des import urls as des_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from rest_framework_swagger.views import get_swagger_view

from sme_ofertaimoveis.imovel.urls import urlpatterns as imovel_urls


env = environ.Env()

schema_view = get_swagger_view(
    title="API de Oferta Imoveis", url=env.str("DJANGO_API_URL", default="")
)

urlpatterns = [
    path("docs/", schema_view, name="docs"),
    path("django-des/", include(des_urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("admin/", admin.site.urls),
    path("api-token-auth/", obtain_jwt_token),
    path("api-token-refresh/", refresh_jwt_token),
    path("", include("apps.home.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ADDING ROUTERS FROM ALL APPS
urlpatterns += imovel_urls
