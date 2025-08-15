from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    re_path(r'^', include(('apps.blog.urls', 'blog'), namespace='blog')),
    re_path(r'^', include(('apps.personal_area.urls', 'personal_area'), namespace='personal_area')),
    path("films/", include(('apps.films.urls', 'films'), namespace='films')),
    re_path(r'^library/', include(('apps.library.urls', 'library'), namespace='library')),
    re_path(r'^summernote/', include('django_summernote.urls')),
    re_path(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
