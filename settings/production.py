from .base import *


DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dc36m579037o5o',
        'USER': 'oydasbujfccaoy',
        'PASSWORD': '57e0fcd11da442f5105e0014ad5250ddc9b3230d69dea01546687e4666cb6490',
        'HOST': 'ec2-54-217-235-137.eu-west-1.compute.amazonaws.com',
        'PORT': '5432',
    }
}