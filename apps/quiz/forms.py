from django import forms
from apps.quiz.models import UserAnswer, Answer


class QuestionForm(forms.Form):
    def __init__(self, question, **kwargs):
        super(QuestionForm, self).__init__(**kwargs)
        self.question = question
        answers = question.answer_set.all()
        choices = tuple((answer.id, answer.text) for answer in answers)
        if answers.filter(right=True).count() > 1:
            widget = forms.CheckboxSelectMultiple(attrs={'class': ''})
            self.fields['answer'] = forms.MultipleChoiceField(choices=choices, widget=widget)
        else:
            widget = forms.RadioSelect(attrs={'class': ''})
            self.fields['answer'] = forms.ChoiceField(choices=choices, widget=widget)

    def save(self, user):
        UserAnswer.objects.filter(question=self.question, user=user).delete()
        answer_ids = self.cleaned_data['answer']
        if type(answer_ids) is str:
            answer_ids = [answer_ids]
        for answer in Answer.objects.filter(id__in=answer_ids):
            user_answer = UserAnswer(user=user, answer=answer, question=self.question)
            user_answer.save()
