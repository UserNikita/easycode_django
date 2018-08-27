from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from apps.personal_area.models import Like


class Category(models.Model):
    title = models.CharField(verbose_name="Название", max_length=255)

    def get_absolute_url(self):
        return reverse('blog:category_post_list', args=(self.id,))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Tag(models.Model):
    name = models.CharField(verbose_name="Название", max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Post(models.Model):
    category = models.ForeignKey(verbose_name="Категория", to='Category', on_delete=models.CASCADE)
    title = models.CharField(verbose_name="Заголовок", max_length=255)
    description = models.TextField(verbose_name="Описание")
    text = models.TextField(verbose_name="Текст")
    slug = models.SlugField(help_text="Строка используемая для формирования url адреса на пост")
    tags = models.ManyToManyField(verbose_name="Теги", to='Tag', blank=True)
    create_date = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    change_date = models.DateTimeField(verbose_name="Дата последнего изменения", auto_now=True)
    draft = models.BooleanField(verbose_name="Черновик", default=False)
    author = models.ForeignKey(verbose_name="Автор", to='auth.User', on_delete=models.CASCADE)
    likes = GenericRelation(to='personal_area.Like', related_query_name='posts')
    comments = GenericRelation(to='personal_area.Comment', related_query_name='posts')

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=(self.id,))

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-create_date',)
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
