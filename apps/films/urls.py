from django.urls import path
from .views import *

urlpatterns = [
    path(
        route="",
        view=FilmListView.as_view(),
        name='films-list'
    ),
    path(
        route="add/",
        view=AddFilmFormView.as_view(),
        name='film-add'
    ),
    path(
        route="<str:pk>/",
        view=FilmDetailView.as_view(),
        name='film-detail'
    ),
    path(
        route="<int:pk>/edit/",
        view=EditFilmFormView.as_view(),
        name='film-edit'
    ),
]
