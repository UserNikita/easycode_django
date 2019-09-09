from django import forms
from django.forms import inlineformset_factory
from django_summernote.widgets import SummernoteWidget
from .models import Question


class QuestionAnswersForm(forms.Form):
    def __init__(self, **kwargs):
        print(kwargs)
        super(QuestionAnswersForm, self).__init__(**kwargs)
        # for answer in question.answer_set.all():
        #     self.fields['answer_%d' % answer.id] = forms.CheckboxInput()
