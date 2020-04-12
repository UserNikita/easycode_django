from django.views.generic import ListView, DetailView
from django.views.generic.edit import BaseFormView

from .forms import *
from .models import *


class QuizListView(ListView):
    template_name = 'quiz/quiz_list.html'
    model = Quiz


class QuizDetailView(DetailView):
    template_name = 'quiz/quiz_detail.html'
    model = Quiz

    def get_context_data(self, **kwargs):
        # TODO: Рефакторить
        context = super().get_context_data(**kwargs)
        quiz = self.get_object()
        yes, no = 0, 0
        for q in quiz.question_set.all():
            if q.get_answer_status(self.request.user) == q.RIGHT:
                yes += 1
            else:
                no += 1
        context['user_stat'] = '[%d, %d]' % (yes, no)

        questions = quiz.question_set.all()
        if questions.exists():
            avg_right_percent = sum([q.get_percent_right_answers() for q in questions]) / questions.count()
            context['total_stat'] = '[%d, %d]' % (avg_right_percent, 100 - avg_right_percent)
        return context


class QuestionDetailView(BaseFormView, DetailView):
    template_name = 'quiz/question_from.html'
    model = Question
    form_class = QuestionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        question = self.get_object()
        if question.get_answer_status(user=self.request.user) != Question.NOT_ANSWERED:
            context['user_answers'] = UserAnswer.objects.filter(user=self.request.user, question=question)
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['question'] = self.get_object()
        return kwargs

    def form_valid(self, form):
        form.save(user=self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        current_question = self.get_object()
        next_question = current_question.quiz.get_next_question(user=self.request.user, question=current_question)
        if next_question is not None:
            return next_question.get_absolute_url()
        else:
            return reverse('quiz:quiz_detail', args=(current_question.quiz.id,))
