from .base import *  # noqa
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env("DJANGO_DEBUG", default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="6fEIQS2aeFhyGongtjqGdLNfjiIhmAdTE8q5UycOPMWbUEDbmiefODftEQBx1mPK",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list(
    "DJANGO_ALLOWED_HOSTS", default=["terceirizadas.sme.prefeitura.sp.gov.br"]
)

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES[0]["OPTIONS"]["debug"] = DEBUG  # noqa F405

# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]

# Your stuff...
# ------------------------------------------------------------------------------
# Para permitir acesso de navegadores sem problema.
CORS_ORIGIN_ALLOW_ALL = True

JWT_AUTH = {
    "JWT_EXPIRATION_DELTA": datetime.timedelta(hours=8),  # noqa
    "JWT_REFRESH_EXPIRATION_DELTA": datetime.timedelta(hours=1),  # noqa
    "JWT_ALLOW_REFRESH": True,
}

URL_HOSTNAME = "http://localhost:8000"
