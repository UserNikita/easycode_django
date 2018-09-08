from django.conf.urls import url, include
from rest_framework import routers
from .api_views import CategoryViewSet, BookViewSet


router = routers.DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('books', BookViewSet)

urlpatterns = [
    url('^', include(router.urls))
]
