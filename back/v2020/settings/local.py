from .base import *
from decouple import config

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*$u!6xj8eo15zd9%^3_8!r%r2&$&-7fd0m3n5w#s2^i5*d%+7x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


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
