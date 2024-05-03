import socket
from settings.base import *


DEBUG = True

ALLOWED_HOSTS = ['*']

ip = socket.gethostbyname(socket.gethostname())
INTERNAL_IPS = [
    '127.0.0.1',
    ip[:-1] + '1',  # tricks to have debug toolbar when developing with docker
]


INSTALLED_APPS += [
    'django_extensions',
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db',
        'USER': 'root',
        'PASSWORD': 'pass',
        'HOST': 'db',
        'PORT': 3306,
    }
}
