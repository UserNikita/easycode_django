from django.conf.urls import url
from .views import *

urlpatterns = [
    url(
        regex=r'^(?P<page>\d*)?/?$',
        view=AssayListView.as_view(),
        name='assay_list'
    ),
    url(
        regex=r'^assay/(?P<pk>\d+)/$',
        view=AssayDetailView.as_view(),
        name='assay_detail'
    ),
    url(
        regex=r'^question/(?P<pk>\d+)/$',
        view=QuestionFormView.as_view(),
        name='question_form'
    ),
    # url(
    #     regex=r'^post/add/$',
    #     view=PostCreateView.as_view(),
    #     name='post_add'
    # ),
    # url(
    #     regex=r'^post/(?P<pk>\d+)/delete/$',
    #     view=PostDeleteView.as_view(),
    #     name='post_delete'
    # ),
]
