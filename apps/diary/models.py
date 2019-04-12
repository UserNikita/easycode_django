from django.db import models


class Note(models.Model):
    user = models.ForeignKey(verbose_name="Пользователь", to='auth.User', on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Текст")
    created = models.DateTimeField(verbose_name="Время создания", auto_now_add=True)
    changed = models.DateTimeField(verbose_name="Время последнего изменения", auto_now=True)

    def __str__(self):
        return ''

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
