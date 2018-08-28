from settings.base import *


DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'easycode$easycode',
        'USER': 'easycode',
        'PASSWORD': 'mysql_passwd',
        'HOST': 'easycode.mysql.pythonanywhere-services.com',
    }
}
