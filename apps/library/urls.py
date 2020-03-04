from django.conf.urls import url
from .views import *

urlpatterns = [
    url(
        regex=r'^(?P<page>\d*)?/?$',
        view=BookListView.as_view(),
        name='book_list'
    ),
    url(
        regex=r'^tag/(?P<tag>\d+)/(?P<page>\d*)?/?$',
        view=TagBookListView.as_view(),
        name='tag_book_list'
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
        regex=r'^book/(?P<pk>\d+)/delete/$',
        view=BookDeleteView.as_view(),
        name='book_delete'
    ),
    url(
        regex=r'^comment/(?P<pk>\d+)/delete/$',
        view=CommentDeleteView.as_view(),
        name='comment_delete'
    ),
    url(
        regex=r'^statistics/$',
        view=StatisticsView.as_view(),
        name='statistics'
    )
]
