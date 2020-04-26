"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 2.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import datetime
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "$yg2c-8-8cszt%3k$b=3wwc^j1g%gn)wj%yldz)6jd(ez80u-s"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# '*'을 넣으면 develop 용으로 모두 허용해준다는데 좀더 봐야할듯.(배포할 땐 허용 가능 호스트를 설정해준다.)
ALLOWED_HOSTS = '*'
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'Access-Control-allow-origin',
    'Access-Control-Allow-Credentials',
    'withcredentials',
    'content-type',
    'cache',
    'Redirect',
    'Authorization'
]
SESSION_COOKIE_SAMESITE_FORCE_ALL = True
# CORS_ALLOW_METHODS = [
#     'DELETE',
#     'GET',
#     'OPTIONS',
#     'PATCH',
#     'POST',
#     'PUT',
# ]

# Application definition
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "api",
    "accounts.apps.AccountsConfig",
    "recommend.apps.RecommendConfig",
    "rest_framework_swagger",
    "corsheaders", #CORS
    "rest_auth", #login auth-start
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'rest_auth.registration',#login auth
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    # 'django_cookies_samesite.middleware.CookiesSameSite',
]

if DEBUG:
    MIDDLEWARE.append("backend.debug.DisableCSRF")

ROOT_URLCONF = "backend.urls"

# 로그인을 위한 설정
SITE_ID = 1
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
REST_AUTH_REGISTER_SERIALIZER = {
    'REGISTER_SERIALIZER' : 'accounts.serializers.MyRegisterSerializer' 
#     # 'LOGIN_SERIALIZER': 'path.to.custom.LoginSerializer',
#     'TOKEN_SERIALIZER': 'accounts.serializers.TokenSerializer',

}
ACCOUNT_EMAIL_REQUIRED = False #로그인할 때 email은 필요없게
REST_USE_JWT = False# JWT사용하자
JWT_AUTH_COOKIE = True
ACCOUNT_LOGOUT_ON_GET = True #get으로 데이터베이스를 바꿀 수 없기 때문에 예외를 둔다
# 로그인을 위한 설정

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_test',
        'USER': 'root',
        'PASSWORD': 'ssafy',
        'HOST': '52.79.223.182',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': 'SET sql_mode="STRICT_TRANS_TABLES"',
            'charset': 'utf8mb4',
            'use_unicode': True
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_L10N = True

USE_TZ = False

# 세션 타임아웃 : 30분으로 설정
SESSION_COOKIE_AGE = 1800

# 사용자의 request가 있는 경우 세션 시간을 연장하고 없는 경우에만 타임아웃 설정
SESSION_SAVE_EVERY_REQUEST = True

# 이전 페이지로 돌아가기
# LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.IsAuthenticated',
    # ),
    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    #     'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    #     'rest_framework.authentication.SessionAuthentication',
    #     'rest_framework.authentication.BasicAuthentication',
    # ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
}


JWT_AUTH = {
    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_ALGORITHM': 'HS256',
    'JWT_ALLOW_REFRESH': True,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(minutes=30),
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=28),
    'JWT_RESPONSE_PAYLOAD_HANDLER':
        'accounts.serializers.jwt_response_payload_handler',
}

PASSWORD_HASHERS = (
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptPasswordHasher",
    "django.contrib.auth.hashers.SHA1PasswordHasher",
    "django.contrib.auth.hashers.MD5PasswordHasher",
    "django.contrib.auth.hashers.CryptPasswordHasher",
)