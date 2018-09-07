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
    next_page = 'blog:post_list'


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


class ProfileUpdateView(UpdateView):
    template_name = 'personal_area/profile_update.html'
    form_class = ProfileForm

    def get_object(self, queryset=None):
        if self.request.user.profile:
            return self.request.user.profile

    def get_initial(self):
        user = self.request.user
        initial_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }
        return initial_data

    def form_valid(self, form):
        user = self.request.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']
        user.save()
        return super(ProfileUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('personal_area:profile_detail')
