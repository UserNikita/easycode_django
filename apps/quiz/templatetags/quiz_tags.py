from django import template
from django.utils.safestring import mark_safe
from apps.quiz.models import *

register = template.Library()


@register.inclusion_tag(filename='quiz/question_nav.html', name='question_nav')
def question_nav(user, quiz, current_question):
    """
    Тег выводит элемент навигации по вопросам викторины
    :param user: пользователь, проходящий тест
    :param quiz: тест, который сейчас проходит данный пользователь
    :param current_question: текущий вопрос на который отвечает пользователь
    :return: html код навигации по вопросам
    """
    context = {
        'user': user,
        'quiz': quiz,
        'current_question': current_question,
    }
    return context


@register.simple_tag()
def get_quiz_start_url(user, quiz):
    """
    Шаблонный тег для получения ссылки на первый вопрос теста
    :param user:
    :param quiz:
    :return: html код для ссылки на первый не отвеченный вопрос теста
    """
    template_string = '<a href="{url}" class="uk-button uk-button-link">{title}</a>'
    start_question = quiz.get_next_question(user=user)
    title = 'Начать' if start_question == quiz.question_set.first() else 'Продолжить'
    if start_question is None:
        return ''
    return mark_safe(template_string.format(url=start_question.get_absolute_url(), title=title))


@register.simple_tag()
def get_answer_status(user, question):
    """
    Тег определяет статус ответа на вопрос для данного пользователя
    :param user: пользователь для которого опрелеояется статус
    :param question: вопрос, статус ответа на который необходимо узнать
    :return: int - константа модели Question
    """
    return question.get_answer_status(user=user)
