from .base import *
from decouple import config

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j9b7^!ini06k49@=22-cy+7jl+4meyonf#yt(y(ks6zzd(-1_t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0', '127.0.0.1']


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
# use this when mysql is the basic db
DATABASES = { 
    'default': {
        'ENGINE': 'django.db.backends.mysql', # mysql 엔진 설정
        'NAME': 'v2020', # 데이터베이스 이름
        'USER': 'root', # 데이터베이스 연결시 사용할 유저 이름
        'PASSWORD': 'root@2020', # 유저 패스워드
        'HOST': '127.0.0.1',
        'PORT': '0',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
            'use_unicode': True,
        },
    }
}


JWT_AUTH = {
    'JWT_PAYLOAD_HANDLER': 'rest_framework_jwt.utils.jwt_payload_handler',
    'JWT_ENCODE_HANDLER': 'rest_framework_jwt.utils.jwt_encode_handler',
    'JWT_DECODE_HANDLER': 'rest_framework_jwt.utils.jwt_decode_handler',
    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_ALGORITHM': 'HS256',
    'JWT_ALLOW_REFRESH': True,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=31),
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_PW')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER