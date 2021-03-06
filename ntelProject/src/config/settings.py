"""
Django settings for ntelProject project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.common/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.common/en/1.10/ref/settings/
"""

import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.common/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'miozo6krang3o%$&%-ts6t5*3+e69eekm+ll!k#qdn4$$k152i'

# SECURITY WARNING: don't run with debug turned on in production!
# 디버그 모드 설정
DEBUG = True

# ALLOWED_HOSTS = ['.ntel.co.kr', '127.0.0.1']  # 서버용
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']  # local용

# Application definition
# pip로 설치한 앱 또는 자신이 만든 app을 추가
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Added Module
    'django_extensions',

    # Added Apps
    'common.apps.CommonConfig',  # 공통 App
    'system.apps.SystemConfig',  # System 관련 App
    'logins.apps.LoginsConfig',  # Login 관련 App
    'appreq.apps.AppreqConfig',  # 이용신청 관련 App
    'main.apps.MainConfig',  # Main App
    'product.apps.ProductConfig',  # 제품 App
    'stock.apps.StockConfig',  # 재고 App
    'open.apps.OpenConfig',  # 개통업무 App
    'plan.apps.PlanConfig',  # 미결업무 App
    'reserve.apps.ReserveConfig',  # 예약업무 App
    'custman.apps.CustmanConfig',  # 고객관리 App
    'receipt.apps.ReceiptConfig',  # 수납/장부 App
    'report.apps.ReportConfig',  # 통계리포트 App
    'setting.apps.SettingConfig',  # 환경설정 App
    'telecom.apps.TelecomConfig',  # 통신사관련 App

    # 시스템관리자 Apps
    'sysman.apps.SysmanConfig',  # 시스템관리자 App

    # Sample Apps
    'sample.apps.SampleConfig',  # 예제 App
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATETIME_INPUT_FORMATS = [
    '%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59'
    '%Y-%m-%d %H:%M:%S.%f',  # '2006-10-25 14:30:59.000200'
    '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
    '%Y-%m-%d',              # '2006-10-25'
    '%Y/%m/%d %H:%M:%S',     # '2006/10/25 14:30:59'
    '%Y/%m/%d %H:%M:%S.%f',  # '2006/10/25 14:30:59.000200'
    '%Y/%m/%d %H:%M',        # '2006/10/25 14:30'
    '%Y/%m/%d',              # '2006/10/25'
    '%y/%m/%d %H:%M:%S',     # '06/10/25 14:30:59'
    '%y/%m/%d %H:%M:%S.%f',  # '06/10/25 14:30:59.000200'
    '%y/%m/%d %H:%M',        # '06/10/25 14:30'
    '%y/%m/%d',              # '06/10/25'
]


WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.common/en/1.10/ref/settings/#databases

DATABASES = {
    # local
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ntel',
        'USER': 'ntel',
        'PASSWORD': '007kkt',
        'HOST': '127.0.0.1',
        'PORT': '3307',
    },
    # dev server
    'dev': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nteldb',
        'USER': 'ntel',
        'PASSWORD': 'baram#315',
        'HOST': '182.162.104.170',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    },
    # local
    'local': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ntel',
        'USER': 'ntel',
        'PASSWORD': '007kkt',
        'HOST': '127.0.0.1',
        'PORT': '3307',
    },
}


# Password validation
# https://docs.djangoproject.common/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.common/en/1.10/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ko-kr'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Seoul'

# USE_TZ = True
USE_TZ = False

USE_I18N = True

USE_L10N = True


PROJECT_DIR = os.path.dirname(__file__)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.common/en/1.10/howto/static-files/
# 정적 파일 의 URL
STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static/')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# Login/out URL
LOGIN_URL = '/logins/login/'  # default '/accounts/login/'
LOOUT_URL = '/logins/logout/'  # default '/accounts/logout/'

# Login 후 이동 URL
LOGIN_REDIRECT_URL = '/main'

# 파일 업로드를 위한 디렉토리
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 브라우저를 닫았을 때 Session 만료처리(default=False)
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Session 만료 시간(5분)
SESSION_COOKIE_AGE = 60 * 30

# CSRF SESSION 사용(Default = False)
CSRF_USE_SESSIONS = False

# Request 요청시 세션 갱신
SESSION_SAVE_EVERY_REQUEST = True

# Customized User
AUTH_USER_MODEL = 'system.SysUser'

######################
# email 관련 smtp -> gmail 이용
######################
# email Host
EMAIL_HOST = 'smtp.gmail.com'
# Port for sending email.
EMAIL_PORT = 587
# HOST User
EMAIL_HOST_USER = 'hisfybabe@gmail.com'
# HOST Password
EMAIL_HOST_PASSWORD = 'grhksxo73!'
# TLS 사용 여부
EMAIL_USE_TLS = True
# 기본 메일 발송자 설정
DEFAULT_FROM_EMAIL = 'ntel5400@naver.com'

ENCRYPTED_FIELDS_KEYDIR = "C:\\ntelProject\\Install\\fieldkeys"
ENCRYPTED_FIELD_KEYS_DIR = "C:\\ntelProject\\Install\\fieldkeys"
