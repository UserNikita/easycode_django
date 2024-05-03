from django.urls import re_path
from .views import *


urlpatterns = [
    re_path(r'^login/$', LoginView.as_view(), name='login'),
    re_path(r'^logout/$', LogoutView.as_view(), name='logout'),
    re_path(r'^registration/$', RegistrationView.as_view(), name='registration'),
    re_path(r'^profile/$', ProfileView.as_view(), name='profile_detail'),
    re_path(r'^profile/edit/$', ProfileUpdateView.as_view(), name='profile_update'),
    # url(r'^profile/edit/$', UserUpdateView.as_view(), name='profile_update'),
]
