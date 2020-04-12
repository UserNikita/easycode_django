from django.conf.urls import url
from .views import *

urlpatterns = [
    url(
        regex=r'^(?P<page>\d*)?/?$',
        view=QuizListView.as_view(),
        name='quiz_list'
    ),
    url(
        regex=r'^(?P<pk>\d+)/result/$',
        view=QuizDetailView.as_view(),
        name='quiz_detail'
    ),
    url(
        regex=r'^question/(?P<pk>\d+)/$',
        view=QuestionDetailView.as_view(),
        name='question_form'
    ),
]
