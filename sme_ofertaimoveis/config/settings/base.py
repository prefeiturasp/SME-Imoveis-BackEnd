"""Base settings to build other settings files upon."""

import datetime
import os

import environ

# (sme_ofertaimoveis/config/settings/base.py - 3 = sme_ofertaimoveis/)
BASE_DIR = environ.Path(__file__) - 4
ROOT_DIR = environ.Path(__file__) - 4
APPS_DIR = ROOT_DIR.path("sme_ofertaimoveis")

env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR.path(".env")))

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True  # env.bool("DJANGO_DEBUG", False)

# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "America/Sao_Paulo"

# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "pt-BR"

# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
LOCALE_PATHS = (os.path.join(ROOT_DIR, "locale"),)
# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": env("POSTGRES_PORT"),
    }
}

DATABASES["default"]["ATOMIC_REQUESTS"] = True

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "sme_ofertaimoveis.config.urls"

# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "sme_ofertaimoveis.config.wsgi.application"

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "corsheaders",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 'django.contrib.humanize', # Handy template tags
    "django.contrib.admin",
]
THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_swagger",
    "des",  # for email configuration in database
    "django_celery_beat",
    'django_xworkflows',
    'sass_processor',
]
LOCAL_APPS = [
    "apps.home",
    "sme_ofertaimoveis.dados_comuns.apps.DadosComunsConfig",
    "sme_ofertaimoveis.users.apps.UsersConfig",
    "sme_ofertaimoveis.imovel.apps.ImovelConfig",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Font Awesome
INSTALLED_APPS += ["fontawesome-free"]

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.BCryptPasswordHasher",
]

# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "users.User"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "users:redirect"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = "account_login"

# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {''
     "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
     },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
DEV_MIDDLEWARE = []

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR("staticfiles"))
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/django_static/"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [str(APPS_DIR.path("static"))]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    'sass_processor.finders.CssFinder',
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR("media"))
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        "DIRS": [str(APPS_DIR.path("templates"))],
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            "debug": DEBUG,
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]
# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = "bootstrap4"

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (str(APPS_DIR.path("fixtures")),)

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="des.backends.ConfiguredEmailBackend"
)
DES_TEST_SUBJECT = "TESTE"
DES_TEST_TEXT_TEMPLATE = os.path.join(APPS_DIR, "templates", "email", "test_email.txt")

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "admin/"
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""Equipe AMCOM|SME""", "equipe-amcom|sme@example.com")]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# Your stuff...
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    # https://www.django-rest-framework.org/api-guide/settings/
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ),
    "DATETIME_FORMAT": "%d/%m/%Y %H:%M:%S",
    "DATETIME_INPUT_FORMATS": ["%d/%m/%Y %H:%M:%S", "iso-8601"],
    "DATE_FORMAT": "%d/%m/%Y",
    "DATE_INPUT_FORMATS": ["%d/%m/%Y", "iso-8601"],
    "TIME_FORMAT": "%H:%M:%S",
    "TIME_INPUT_FORMATS": ["%H:%M:%S", "iso-8601"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}

URL_CONFIGS = {
    'RECUPERAR_SENHA': 'recuperar-senha?uuid={uuid}&confirmationKey={confirmation_key}'
}

SWAGGER_SETTINGS = {
    "LOGIN_URL": "rest_framework:login",
    "LOGOUT_URL": "rest_framework:logout",
    "USE_SESSION_AUTH": True,
    "DOC_EXPANSION": "list",
    "APIS_SORTER": "alpha",
    "SECURITY_DEFINITIONS": None,
}

JWT_AUTH = {
    # TODO: rever a configuração...
    "JWT_EXPIRATION_DELTA": datetime.timedelta(hours=100),
    "JWT_REFRESH_EXPIRATION_DELTA": datetime.timedelta(hours=100),
    "JWT_ALLOW_REFRESH": True,
}

FILA_CRECHE_URL = "https://filadacreche.sme.prefeitura.sp.gov.br"
SCIEDU_URL = env("SCIEDU_URL")
SCIEDU_TOKEN = env("SCIEDU_TOKEN")
FILA_CRECHE_GRUPOS = (
    (1, "Bercario I"),
    (4, "Bercario II"),
    (27, "Mini Grupo I"),
    (28, "Mini grupo II"),
)


# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}


# CELERY SETTINGS
CELERY_REDIS_URL = env("CELERY_REDIS_URL")
CELERY_BROKER_URL = f"{CELERY_REDIS_URL}/0"
CELERY_BACKEND = f"{CELERY_REDIS_URL}/1"
CELERY_RESULT_BACKEND = CELERY_REDIS_URL

CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_ENABLE_UTC = True

URL_HOSTNAME = ""

SME_INTEGRACAO_URL = env('SME_INTEGRACAO_URL')
SME_INTEGRACAO_TOKEN = env('SME_INTEGRACAO_TOKEN')

EOL_API_TERCEIRIZADAS_URL = env('EOL_API_TERCEIRIZADAS_URL')
EOL_API_TERCEIRIZADAS_TOKEN = env('EOL_API_TERCEIRIZADAS_TOKEN')
