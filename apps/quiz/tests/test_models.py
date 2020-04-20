from django.test import TestCase, tag
from django.contrib.auth.models import User
from apps.quiz.models import *

class ModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        admin_credentials = {
            'email': 'admin@localhost.ru',
            'username': 'admin',
            'password': '123456'
        }
        user_credentials = {
            'email': 'user@localhost.ru',
            'username': 'user',
            'password': '123456'
        }
        cls.admin = User.objects.create_superuser(**admin_credentials)
        cls.user = User.objects.create_user(**user_credentials)

    # def setUp(self):
    #     self.quiz = Quiz.objects.create(name='Quiz')
    #
    #     self.question1 = Question.objects.create(quiz=self.quiz, text='q1')
    #     self.question2 = Question.objects.create(quiz=self.quiz, text='q2')
    #
    #     self.answer1 = Answer.objects.create(question=self.question1, text='q1a1', right=True)
    #     self.answer2 = Answer.objects.create(question=self.question1, text='q1a2', right=False)
    #     self.answer3 = Answer.objects.create(question=self.question1, text='q1a3', right=False)
    #     self.answer4 = Answer.objects.create(question=self.question2, text='q2a4', right=True)
    #     self.answer5 = Answer.objects.create(question=self.question2, text='q2a5', right=True)
    #     self.answer6 = Answer.objects.create(question=self.question2, text='q2a6', right=False)


class AnswerTestCase(ModelTestCase):
    def setUp(self):
        self.quiz = Quiz.objects.create(name='Quiz')
        self.question = Question.objects.create(quiz=self.quiz, text='q')
        self.answer = Answer.objects.create(question=self.question, text='a', right=True)

    def test_answer_get_users_passed(self):
        self.assertEqual(self.answer.users.count(), 0)
        UserAnswer.objects.create(user=self.user, question=self.answer.question, answer=self.answer)
        self.assertEqual(self.answer.users.count(), 1)


class QuestionWithOneRightAnswerTestCase(ModelTestCase):
    def setUp(self):
        self.quiz = Quiz.objects.create(name='Quiz')
        self.question = Question.objects.create(quiz=self.quiz, text='q')
        self.answer1 = Answer.objects.create(question=self.question, text='a1', right=True)
        self.answer2 = Answer.objects.create(question=self.question, text='a2', right=False)

    def test_status_not_answered(self):
        # Пользователь не выбрал ни один ответ
        status = self.question.get_answer_status(user=self.user)
        self.assertEqual(status, Question.NOT_ANSWERED)

    def test_status_right(self):
        # Пользователь выбрал правильный ответ
        UserAnswer.objects.create(user=self.user, question=self.question, answer=self.answer1)
        status = self.question.get_answer_status(user=self.user)
        self.assertEqual(status, Question.RIGHT)

    def test_status_not_right(self):
        # Пользователь выбрал неправильный ответ
        UserAnswer.objects.create(user=self.user, question=self.question, answer=self.answer2)
        status = self.question.get_answer_status(user=self.user)
        self.assertEqual(status, Question.NOT_RIGHT)

    def test_status_not_right_with_different_answers(self):
        # Пользователь выбрал правильный и неправильный ответы
        UserAnswer.objects.create(user=self.user, question=self.question, answer=self.answer1)
        UserAnswer.objects.create(user=self.user, question=self.question, answer=self.answer2)
        status = self.question.get_answer_status(user=self.user)
        self.assertEqual(status, Question.NOT_RIGHT)

    def test_percent_right_answers_if_not_answered(self):
        # На вопрос ещё никто не ответил, то процент правильных ответов 0
        percent = self.question.get_percent_right_answers()
        self.assertEqual(percent, 0)

    def test_percent_right_answers_if_not_right_answers(self):
        # Есть только неправильные ответы
        UserAnswer.objects.create(user=self.user, question=self.question, answer=self.answer2)
        UserAnswer.objects.create(user=self.admin, question=self.question, answer=self.answer2)
        percent = self.question.get_percent_right_answers()
        self.assertEqual(percent, 0)

    def test_percent_right_answers_if_right_answers(self):
        # Есть только правильные ответы
        UserAnswer.objects.create(user=self.user, question=self.question, answer=self.answer1)
        UserAnswer.objects.create(user=self.admin, question=self.question, answer=self.answer1)
        percent = self.question.get_percent_right_answers()
        self.assertEqual(percent, 100)

    def test_percent_right_answers_if_different_answers(self):
        # Есть и правильные и неправильные ответы
        UserAnswer.objects.create(user=self.user, question=self.question, answer=self.answer1)
        UserAnswer.objects.create(user=self.admin, question=self.question, answer=self.answer2)
        percent = self.question.get_percent_right_answers()
        self.assertEqual(percent, 50)


class QuestionWithManyRightAnswerTestCase(ModelTestCase):
    def setUp(self):
        self.quiz = Quiz.objects.create(name='Quiz')
        self.question = Question.objects.create(quiz=self.quiz, text='q')
        self.answer1 = Answer.objects.create(question=self.question, text='a1', right=True)
        self.answer2 = Answer.objects.create(question=self.question, text='a2', right=True)
        self.answer3 = Answer.objects.create(question=self.question, text='a3', right=False)

    def test_status_not_answered(self):
        # Пользователь не выбрал ни один ответ
        status = self.question.get_answer_status(user=self.user)
        self.assertEqual(status, Question.NOT_ANSWERED)

    def test_status_right(self):
        # Пользователь выбрал правильные ответы
        UserAnswer.objects.create(user=self.user, question=self.question, answer=self.answer1)
        UserAnswer.objects.create(user=self.user, question=self.question, answer=self.answer2)
        status = self.question.get_answer_status(user=self.user)
        self.assertEqual(status, Question.RIGHT)

    def test_status_not_right_because_selected_one_answer(self):
        # Пользователь выбрал только один правильный ответ
        UserAnswer.objects.create(user=self.user, question=self.question, answer=self.answer1)
        status = self.question.get_answer_status(user=self.user)
        self.assertEqual(status, Question.NOT_RIGHT)

    def test_status_not_right_because_selected_not_right_answer(self):
        # Пользователь выбрал неправильный ответ
        UserAnswer.objects.create(user=self.user, question=self.question, answer=self.answer3)
        status = self.question.get_answer_status(user=self.user)
        self.assertEqual(status, Question.NOT_RIGHT)

    def test_status_not_right_because_selected_not_right_answer_and_all_right_answers(self):
        # Пользователь выбрал неправильный ответ вместе с правильными
        UserAnswer.objects.create(user=self.user, question=self.question, answer=self.answer1)
        UserAnswer.objects.create(user=self.user, question=self.question, answer=self.answer2)
        UserAnswer.objects.create(user=self.user, question=self.question, answer=self.answer3)
        status = self.question.get_answer_status(user=self.user)
        self.assertEqual(status, Question.NOT_RIGHT)
