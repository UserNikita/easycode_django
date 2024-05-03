from django.urls import re_path
from .views import *

urlpatterns = [
    re_path(
        route=r'^(?P<page>\d*)?/?$',
        view=PostListView.as_view(),
        name='post_list'
    ),
    re_path(
        route=r'^category/(?P<category>\d+)/(?P<page>\d*)?/?$',
        view=CategoryPostListView.as_view(),
        name='category_post_list'
    ),
    re_path(
        route=r'^post/(?P<pk>\d+)/$',
        view=PostDetailView.as_view(),
        name='post_detail'
    ),
    re_path(
        route=r'^post/(?P<pk>\d+)/edit/$',
        view=PostUpdateView.as_view(),
        name='post_edit'
    ),
    re_path(
        route=r'^post/add/$',
        view=PostCreateView.as_view(),
        name='post_add'
    ),
    re_path(
        route=r'^post/(?P<pk>\d+)/delete/$',
        view=PostDeleteView.as_view(),
        name='post_delete'
    ),
    re_path(
        route=r'^comment/(?P<pk>\d+)/delete/$',
        view=CommentDeleteView.as_view(),
        name='comment_delete'
    ),
]
