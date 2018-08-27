from django.conf.urls import url
from .views import *

urlpatterns = [
    url(
        regex=r'^(?P<page>\d*)?/?$',
        view=BookListView.as_view(),
        name='book_list'
    ),
    url(
        regex=r'^category/(?P<category>\d+|none)/(?P<page>\d*)?/?$',
        view=CategoryBookListView.as_view(),
        name='category_book_list'
    ),
    url(
        regex=r'^book/(?P<pk>\d+)/$',
        view=BookDetailView.as_view(),
        name='book_detail'
    ),
    url(
        regex=r'^book/(?P<pk>\d+)/edit/$',
        view=BookUpdateView.as_view(),
        name='book_edit'
    ),
    url(
        regex=r'^book/add/$',
        view=BookCreateView.as_view(),
        name='book_create'
    ),
    url(
        regex=r'^post/(?P<pk>\d+)/delete/$',
        view=BookDeleteView.as_view(),
        name='book_delete'
    ),
]
