from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.templatetags.static import static


class Profile(models.Model):
    user = models.OneToOneField(verbose_name='Пользователь', to='auth.User', on_delete=models.CASCADE)
    photo = models.ImageField(verbose_name='Фото', blank=True)

    def __str__(self):
        return f"Профиль: {self.user}"

    def get_photo_url(self):
        if self.photo and self.photo.url:
            return self.photo.url
        return static('img/default_avatar.jpg')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Like(models.Model):
    limit = models.Q(app_label='library', model='book') | models.Q(app_label='blog', model='post')

    user = models.ForeignKey(verbose_name="Пользователь", to='auth.User', on_delete=models.CASCADE)
    creation_date = models.DateTimeField(verbose_name="Дата создания", auto_now=True)

    content_type = models.ForeignKey(to='contenttypes.ContentType', limit_choices_to=limit, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type', fk_field='object_id')

    def __str__(self):
        return str(self.content_type)

    class Meta:
        unique_together = ('user', 'object_id', 'content_type')
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"


class Comment(models.Model):
    limit = models.Q(app_label='library', model='book') | models.Q(app_label='blog', model='post')

    text = models.TextField(verbose_name="Текст")
    author = models.ForeignKey(verbose_name="Автор", to='auth.User', on_delete=models.CASCADE)
    creation_date = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)

    content_type = models.ForeignKey(to='contenttypes.ContentType', limit_choices_to=limit, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type', fk_field='object_id')

    def __str__(self):
        return str(self.content_type)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
