from django.conf.urls import url
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    url(r'^', include(('apps.blog.urls', 'blog'), namespace='blog')),
    url(r'^', include(('apps.personal_area.urls', 'personal_area'), namespace='personal_area')),
    url(r'^library/', include(('apps.library.urls', 'library'), namespace='library')),
    url(r'^summernote/', include('django_summernote.urls')),
    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
