from django.views.generic import FormView, RedirectView, TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from .forms import *


class LoginView(BaseLoginView):
    template_name = 'personal_area/login.html'
    authentication_form = LoginForm


class LogoutView(BaseLogoutView):
    next_page = 'personal_area:login'


class RegistrationView(FormView):
    template_name = 'personal_area/registration.html'
    form_class = RegistrationForm
    success_url = '/'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super(RegistrationView, self).form_valid(form)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'personal_area/profile_detail.html'


class UserUpdateView(UpdateView):
    template_name = 'personal_area/profile_update.html'
    model = User
    form_class = UserChangeForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('personal_area:profile_detail')


class ProfileUpdateView(UpdateView):
    template_name = 'personal_area/profile_change_photo.html'
    form_class = ProfileForm

    def get_object(self, queryset=None):
        if self.request.user.profile:
            return self.request.user.profile

    def get_success_url(self):
        return reverse('personal_area:profile_detail')
