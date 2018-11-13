from django.db import models


class Question(models.Model):
    text = models.TextField(verbose_name="Текст вопроса")

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class Answer(models.Model):
    question = models.ForeignKey(verbose_name="Вопрос", to='Question', on_delete=models.SET_NULL, null=True, blank=True)
    text = models.CharField(verbose_name="Текст ответа", max_length=255)
    correct = models.BooleanField(verbose_name="Правильный ответ", default=False)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"
