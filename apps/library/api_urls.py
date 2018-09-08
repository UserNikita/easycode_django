from django.conf.urls import url, include
from rest_framework import routers
from .api_views import *


router = routers.DefaultRouter()
router.register('category', CategoryViewSet)

urlpatterns = [
    url('^', include(router.urls))
]
