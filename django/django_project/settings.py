"""
Django settings for icosa project.
Generated by 'django-admin startproject' using Django 4.2.11.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
if os.environ.get("DJANGO_DISABLE_CACHE"):
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    }

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
JWT_KEY = os.environ.get("JWT_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEPLOYMENT_ENV = os.environ.get("DEPLOYMENT_ENV")
DEPLOYMENT_HOST_WEB = os.environ.get("DEPLOYMENT_HOST_WEB")
DEPLOYMENT_HOST_API = os.environ.get("DEPLOYMENT_HOST_API")
DEBUG = False
if DEPLOYMENT_ENV in [
    "development",
    "local",
]:
    DEBUG = True

SITE_ID = 1

ALLOWED_HOSTS = [
    "localhost",
    f"{DEPLOYMENT_HOST_WEB}",
]

if DEPLOYMENT_HOST_API:
    ALLOWED_HOSTS.append(f"{DEPLOYMENT_HOST_API}")

CSRF_TRUSTED_ORIGINS = [
    "https://*.127.0.0.1",
    f"https://{DEPLOYMENT_HOST_WEB}",
]

if DEPLOYMENT_HOST_API:
    CSRF_TRUSTED_ORIGINS.append(f"https://{DEPLOYMENT_HOST_API}")

DJANGO_DEFAULT_FILE_STORAGE = os.environ.get("DJANGO_DEFAULT_FILE_STORAGE")
DJANGO_STORAGE_URL = os.environ.get("DJANGO_STORAGE_URL")
DJANGO_STORAGE_BUCKET_NAME = os.environ.get("DJANGO_STORAGE_BUCKET_NAME")
DJANGO_STORAGE_REGION_NAME = os.environ.get("DJANGO_STORAGE_REGION_NAME")
DJANGO_STORAGE_ACCESS_KEY = os.environ.get("DJANGO_STORAGE_ACCESS_KEY")
DJANGO_STORAGE_SECRET_KEY = os.environ.get("DJANGO_STORAGE_SECRET_KEY")

if (
    DJANGO_STORAGE_URL
    and DJANGO_STORAGE_BUCKET_NAME
    and DJANGO_STORAGE_REGION_NAME
    and DJANGO_STORAGE_ACCESS_KEY
    and DJANGO_STORAGE_SECRET_KEY
):

    # Not using the STORAGES dict here as there is a bug in django-storages
    # that means we must set these separately.
    DEFAULT_FILE_STORAGE = DJANGO_DEFAULT_FILE_STORAGE
    AWS_DEFAULT_ACL = "public-read"
    AWS_ACCESS_KEY_ID = DJANGO_STORAGE_ACCESS_KEY
    AWS_SECRET_ACCESS_KEY = DJANGO_STORAGE_SECRET_KEY
    AWS_STORAGE_BUCKET_NAME = DJANGO_STORAGE_BUCKET_NAME
    AWS_S3_REGION_NAME = DJANGO_STORAGE_REGION_NAME
    AWS_S3_ENDPOINT_URL = DJANGO_STORAGE_URL
else:
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

STAFF_ONLY_ACCESS = os.environ.get("DJANGO_STAFF_ONLY_ACCESS")

# Application definition

APPEND_SLASH = False

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "django.contrib.messages",
    "constance",
    "constance.backends.database",
    "icosa",
    "honeypot",
    "maintenance_mode",
    "compressor",
    "corsheaders",
    "huey.contrib.djhuey",
]

MIDDLEWARE = [
    "django.middleware.gzip.GZipMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "icosa.middleware.redirect.RemoveSlashMiddleware",
    "maintenance_mode.middleware.MaintenanceModeMiddleware",
]

ROOT_URLCONF = "django_project.urls"
LOGIN_URL = "/login"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "icosa.context_processors.settings_processor",
                "constance.context_processors.config",
                "icosa.context_processors.owner_processor",
            ],
            "loaders": [
                "django.template.loaders.app_directories.Loader",
            ],
        },
    },
]

EMAIL_HOST = os.environ.get("DJANGO_EMAIL_HOST", "localhost")
EMAIL_HOST_USER = os.environ.get("DJANGO_EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("DJANGO_EMAIL_HOST_PASSWORD", "")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.environ.get("DJANGO_DEFAULT_FROM_EMAIL", "")
ADMIN_EMAIL = os.environ.get("DJANGO_ADMIN_EMAIL", None)

WSGI_APPLICATION = "django_project.wsgi.application"

PAGINATION_PER_PAGE = 40

ACCESS_TOKEN_EXPIRE_MINUTES = 20_160  # 2 weeks

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": "db",
        "PORT": 5432,
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

# Media files
# TODO make this configurable based on file storage. We should have an absolute
# path for local storage and a root-relative path for storages such as s3.
MEDIA_ROOT = "icosa"
# MEDIA_URL = "..."  # unused with django-storages

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Cors settings

CORS_ALLOW_ALL_ORIGINS = bool(
    os.environ.get("DJANGO_CORS_ALLOW_ALL_ORIGINS", False)
)

if os.environ.get("DJANGO_CORS_ALLOWED_ORIGINS", None) is not None:
    CORS_ALLOWED_ORIGINS = [
        x
        for x in os.environ.get(
            "DJANGO_CORS_ALLOWED_ORIGINS",
            "",
        ).split(",")
        if x
    ]

# Compressor settings

COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)

# Constance settings

CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"
CONSTANCE_CONFIG = {
    "BETA_MODE": (
        True,
        "Sets various text around the site, inc. the logo in the header",
        bool,
    ),
    "REGISTRATION_ALLOW_LIST": (
        "",
        "Comma-separated list of email addresses. When populated, will only allow these email addresses to register new accounts.",
        str,
    ),
}

# Debug Toolbar settings

DEBUG_TOOLBAR_ENABLED = True

DEBUG_TOOLBAR_URL_EXCLUDE: tuple[str] = ()

if DEBUG_TOOLBAR_ENABLED:
    INSTALLED_APPS = [
        "debug_toolbar",
    ] + INSTALLED_APPS

    MIDDLEWARE.remove(
        "django.middleware.gzip.GZipMiddleware",
    )
    MIDDLEWARE.remove(
        "django.contrib.auth.middleware.AuthenticationMiddleware",
    )
    MIDDLEWARE.remove(
        "django.contrib.sessions.middleware.SessionMiddleware",
    )

    MIDDLEWARE = [
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.middleware.gzip.GZipMiddleware",
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ] + MIDDLEWARE

    INTERNAL_IPS = ["127.0.0.1"]

    def show_toolbar(request):
        """Put 'debug=on' or 'debug=1' in a query string to enable debugging for
        your current session. 'debug=off' will turn it off again.
        """
        if request.path in DEBUG_TOOLBAR_URL_EXCLUDE:
            # No point going any further if it's an excluded Url
            return False
        debug_flag = request.GET.get("debug")
        if debug_flag == "on" or debug_flag == "1":
            request.session["show_debug_toolbar"] = True
        elif debug_flag == "off" or debug_flag == "0":
            request.session["show_debug_toolbar"] = False
        session_debug = request.session.get("show_debug_toolbar", False)
        if request.user.is_superuser and session_debug:
            return True
        return False

    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": show_toolbar,
    }

# Honeypot settings

HONEYPOT_FIELD_NAME = "asset_ref"

# Huey settings

HUEY = {
    "huey_class": "huey.SqliteHuey",  # Huey implementation to use.
    "results": True,  # Store return values of tasks.
    "store_none": False,  # If a task returns None, do not save to results.
    "immediate": False,
    "utc": True,  # Use UTC for all times internally.
    "consumer": {
        "workers": 1,
        "worker_type": "thread",
        "initial_delay": 0.1,  # Smallest polling interval, same as -d.
        "backoff": 1.15,  # Exponential backoff using this rate, -b.
        "max_delay": 10.0,  # Max possible polling interval, -m.
        "scheduler_interval": 1,  # Check schedule every second, -s.
        "periodic": True,  # Enable crontab feature.
        "check_worker_health": True,  # Enable worker health checks.
        "health_check_interval": 1,  # Check worker health every second.
    },
}

# Note: Huey has its own setting to disable the task queue, but this still
# calls the same code in userland. ENABLE_TASK_QUEUE is useful for excluding
# huey from the code path entirely.

ENABLE_TASK_QUEUE = os.environ.get("DJANGO_ENABLE_TASK_QUEUE", True)

# Maintenance Mode settings

MAINTENANCE_MODE = os.environ.get("DJANGO_MAINTENANCE_MODE", False)
MAINTENANCE_MODE_IGNORE_STAFF = True
MAINTENANCE_MODE_IGNORE_URLS = ["/admin/", "/device/", "/v1/"]

# Ninja settings

NINJA_PAGINATION_PER_PAGE = 20

# Category settings
#
# Google Poly originally came with a set of categories that were not
# user-editable. The official install of Icosa Gallery respects these, but
# allows user installations to override them in settings. To avoid hard-coding
# the categories, which would result in a migration and source code changes to
# amend them, we are instead mapping from an int to a string here.
ASSET_CATEGORIES_MAP = {
    1: ("Art", "art"),
    2: ("Animals & Pets", "animals"),
    3: ("Architecture", "architecture"),
    4: ("Places & Scenes", "places"),
    5: ("Unused", "unused"),
    6: ("Food & Drink", "food"),
    7: ("Nature", "nature"),
    8: ("People & Characters", "people"),
    9: ("Tools & Technology", "tech"),
    10: ("Transport", "transport"),
    11: ("Miscellaneous", "miscellaneous"),
    12: ("Objects", "objects"),
    13: ("Culture & Humanity", "culture"),
    14: ("Current Events", "current_events"),
    15: ("Furniture & Home", "home"),
    16: ("History", "history"),
    17: ("Science", "science"),
    18: ("Sports & Fitness", "sport"),
    19: ("Travel & Leisure", "travel"),
}
# TODO(james): move this to somewhere else so that categories can be overridden
# in local settings and still be reverse mapped correctly.
ASSET_CATEGORIES_REVERSE_MAP = {
    v[1]: k for k, v in ASSET_CATEGORIES_MAP.items()
}
ASSET_CATEGORY_LABEL_MAP = {
    v[1]: v[0] for k, v in ASSET_CATEGORIES_MAP.items()
}
