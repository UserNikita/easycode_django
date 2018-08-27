from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^registration/$', RegistrationView.as_view(), name='registration'),
    url(r'^profile/$', ProfileView.as_view(), name='profile_detail'),
    url(r'^profile/edit/$', UserUpdateView.as_view(), name='profile_update'),
    url(r'^profile/photo/edit/$', ProfileUpdateView.as_view(),
        name='profile_photo_update'),
]
