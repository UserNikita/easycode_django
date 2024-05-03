from django.urls import re_path
from .views import *

urlpatterns = [
    re_path(
        route=r'^(?P<page>\d*)?/?$',
        view=BookListView.as_view(),
        name='book_list'
    ),
    re_path(
        route=r'^tag/(?P<tag>\d+)/(?P<page>\d*)?/?$',
        view=TagBookListView.as_view(),
        name='tag_book_list'
    ),
    re_path(
        route=r'^book/(?P<pk>\d+)/$',
        view=BookDetailView.as_view(),
        name='book_detail'
    ),
    re_path(
        route=r'^book/(?P<pk>\d+)/edit/$',
        view=BookUpdateView.as_view(),
        name='book_edit'
    ),
    re_path(
        route=r'^book/add/$',
        view=BookCreateView.as_view(),
        name='book_create'
    ),
    re_path(
        route=r'^book/(?P<pk>\d+)/delete/$',
        view=BookDeleteView.as_view(),
        name='book_delete'
    ),
    re_path(
        route=r'^comment/(?P<pk>\d+)/delete/$',
        view=CommentDeleteView.as_view(),
        name='comment_delete'
    ),
    re_path(
        route=r'^statistics/$',
        view=StatisticsView.as_view(),
        name='statistics'
    )
]
