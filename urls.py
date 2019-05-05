"""Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    url(r'^', include(('apps.blog.urls', 'blog'), namespace='blog')),
    url(r'^', include(('apps.personal_area.urls', 'personal_area'), namespace='personal_area')),
    url(r'^library/', include(('apps.library.urls', 'library'), namespace='library')),
    url(r'^api/library/', include(('apps.library.api_urls', 'library_api'), namespace='library_api')),
    url(r'^assay/', include(('apps.assay.urls', 'assay'), namespace='assay')),
    url(r'^summernote/', include('django_summernote.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
