from .base import *
from decouple import config

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['0.0.0.0']


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
# use this when mysql is the basic db
DATABASES = { 
    'default': {
        'ENGINE': 'django.db.backends.mysql', # mysql 엔진 설정
        'NAME': config('DB_NAME'), # 데이터베이스 이름
        'USER': config('DB_USER'), # 데이터베이스 연결시 사용할 유저 이름
        'PASSWORD': config('DB_PW'), # 유저 패스워드
        'HOST': '127.0.0.1',
        'PORT': '',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
            'use_unicode': True,
        },
    }
}
