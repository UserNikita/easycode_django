from django.db import models
from django.urls import reverse


class Quiz(models.Model):
    name = models.CharField(verbose_name="Название теста", max_length=255)

    users_passed = models.ManyToManyField(verbose_name="Пользователи прошедшие тест", to='auth.User', blank=True)

    def get_absolute_url(self):
        return reverse('quiz:quiz_detail', args=(self.id,))

    def get_user_tested_count(self):
        return UserAnswer.objects.filter(answer__question__quiz=self).values_list('user_id').distinct().count()

    def get_next_question(self, user, question=None):
        question_qs = self.question_set.all() if question is None else self.question_set.filter(id__gt=question.id)
        for q in question_qs:
            if q.get_answer_status(user=user) == Question.NOT_ANSWERED:
                return q
        return None

    def get_user_progress(self, user):
        statuses = {
            Question.NOT_ANSWERED: 0,
            Question.RIGHT: 0,
            Question.NOT_RIGHT: 0,
        }
        for question in self.question_set.all():
            statuses[question.get_answer_status(user)] += 1
        return statuses

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"


class Question(models.Model):
    NOT_ANSWERED = 0
    RIGHT = 1
    NOT_RIGHT = 2

    quiz = models.ForeignKey(verbose_name="Тест", to='Quiz', on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Текст вопроса")

    def get_absolute_url(self):
        return reverse('quiz:question_form', args=(self.id,))

    def get_answer_status(self, user):
        user_answers = set(self.answer_set.filter(useranswer__user=user).values_list('id', flat=True))
        if len(user_answers) == 0:
            return self.NOT_ANSWERED
        right_answers = set(self.answer_set.filter(right=True).values_list('id', flat=True))
        if user_answers == right_answers:
            return self.RIGHT
        return self.NOT_RIGHT

    def get_percent_right_answers(self):
        right_users = set(UserAnswer.objects.filter(answer__in=self.answer_set.filter(right=True))
                          .values_list('user_id', flat=True))
        not_right_users = set(UserAnswer.objects.filter(answer__in=self.answer_set.filter(right=False))
                              .values_list('user_id', flat=True))

        all_user_answers_count = len(right_users) + len(not_right_users)
        right_user_answers_count = len(right_users - not_right_users)

        if all_user_answers_count > 0:
            return right_user_answers_count / (all_user_answers_count / 100)
        return 0

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class Answer(models.Model):
    question = models.ForeignKey(verbose_name="Вопрос", to='Question', on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Текст ответа")
    right = models.BooleanField(verbose_name="Правильный ответ", default=False)
    users = models.ManyToManyField(verbose_name="Пользователи", to='auth.User', through='UserAnswer', blank=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"


class UserAnswer(models.Model):
    user = models.ForeignKey(verbose_name="", to='auth.User', on_delete=models.CASCADE)
    question = models.ForeignKey(verbose_name="", to='Question', on_delete=models.CASCADE)
    answer = models.ForeignKey(verbose_name="", to='Answer', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Ответ пользователя"
        verbose_name_plural = "Ответы пользователей"
