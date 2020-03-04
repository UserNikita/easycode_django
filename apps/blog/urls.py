from django.conf.urls import url
from .views import *

urlpatterns = [
    url(
        regex=r'^(?P<page>\d*)?/?$',
        view=PostListView.as_view(),
        name='post_list'
    ),
    url(
        regex=r'^category/(?P<category>\d+)/(?P<page>\d*)?/?$',
        view=CategoryPostListView.as_view(),
        name='category_post_list'
    ),
    url(
        regex=r'^post/(?P<pk>\d+)/$',
        view=PostDetailView.as_view(),
        name='post_detail'
    ),
    url(
        regex=r'^post/(?P<pk>\d+)/edit/$',
        view=PostUpdateView.as_view(),
        name='post_edit'
    ),
    url(
        regex=r'^post/add/$',
        view=PostCreateView.as_view(),
        name='post_add'
    ),
    url(
        regex=r'^post/(?P<pk>\d+)/delete/$',
        view=PostDeleteView.as_view(),
        name='post_delete'
    ),
    url(
        regex=r'^comment/(?P<pk>\d+)/delete/$',
        view=CommentDeleteView.as_view(),
        name='comment_delete'
    ),
]
