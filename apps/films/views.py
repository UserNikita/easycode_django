from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from apps.films.models import Film
from apps.films.forms import FilmForm


class FilmListView(LoginRequiredMixin, ListView):
    template_name = "films/list_films.html"
    context_object_name = "film_list"
    model = Film


class FilmDetailView(LoginRequiredMixin, DetailView):
    template_name = "films/detail_film.html"
    context_object_name = "film"
    model = Film


class AddFilmFormView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = "films/add_film.html"
    form_class = FilmForm

    def test_func(self):
        return self.request.user.is_staff


class EditFilmFormView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "films/edit_film.html"
    form_class = FilmForm
    queryset = Film.objects.all()

    def test_func(self):
        return self.request.user.is_staff
