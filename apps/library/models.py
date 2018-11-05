from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse
from django.templatetags.static import static
from django.utils.safestring import mark_safe

FILE_FORMATS = (
    (0, 'PDF'),
    (1, 'DJVU'),
)

BACKGROUND_COLORS = (
    ("bgm-white", "White"),
    ("bgm-black", "Black"),
    ("bgm-brown", "Brown"),
    ("bgm-pink", "Pink"),
    ("bgm-red", "Red"),
    ("bgm-blue", "Blue"),
    ("bgm-purple", "Purple"),
    ("bgm-deeppurple", "Deep purple"),
    ("bgm-lightblue", "Light blue"),
    ("bgm-cyan", "Cyan"),
    ("bgm-teal", "Teal"),
    ("bgm-green", "Green"),
    ("bgm-lightgreen", "Light green"),
    ("bgm-lime", "Lime"),
    ("bgm-yellow", "Yellow"),
    ("bgm-amber", "Amber"),
    ("bgm-orange", "Orange"),
    ("bgm-deeporange", "Deep orange"),
    ("bgm-gray", "Gray"),
    ("bgm-bluegray", "Blue gray"),
    ("bgm-indigo", "Indigo"),
)


class Book(models.Model):
    title = models.CharField(verbose_name="Название", max_length=500)
    description = models.TextField(verbose_name="Описание", blank=True)
    cover = models.ImageField(verbose_name="Обложка", blank=True)
    authors = models.ManyToManyField(verbose_name="Авторы", to='Author')
    publishers = models.ManyToManyField(verbose_name="Издательства", to='Publisher')
    year = models.PositiveIntegerField(verbose_name="Год издания")
    category = models.ForeignKey(verbose_name="Категория", to='Category', blank=True, null=True,
                                 on_delete=models.SET_NULL)
    tags = models.ManyToManyField(verbose_name="Теги", to='Tag', blank=True)
    page_count = models.PositiveSmallIntegerField(verbose_name="Количество страниц", default=0)
    draft = models.BooleanField(verbose_name="Черновик", default=False)
    created_date = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    changed_date = models.DateTimeField(verbose_name="Дата последнего изменения", auto_now=True)

    likes = GenericRelation(to='personal_area.Like', related_query_name='books')
    comments = GenericRelation(to='personal_area.Comment', related_query_name='books')

    def get_absolute_url(self):
        return reverse('library:book_detail', args=(self.id,))

    def get_cover_url(self):
        if self.cover:
            return self.cover.url
        return static('img/missing_book_cover.jpg')

    def get_cover(self):
        img_html_tag = '<img src="%s" width="50px">' % self.get_cover_url()
        return mark_safe(img_html_tag)

    get_cover.short_description = "Обложка"

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-id',)
        verbose_name = "Книга"
        verbose_name_plural = "Книги"


class BookFile(models.Model):
    book = models.ForeignKey(to='Book', verbose_name='Книга', on_delete=models.CASCADE)
    url = models.URLField(verbose_name='Ссылка для скачивания')
    size = models.FloatField(verbose_name='Размер файла', help_text='Условный размер файла в мегабайтах')
    format = models.PositiveSmallIntegerField(verbose_name='Формат файла', choices=FILE_FORMATS, default=0)

    def __str__(self):
        return self.book.title

    class Meta:
        verbose_name = 'Файл книги'
        verbose_name_plural = 'Файлы книг'


class Author(models.Model):
    full_name = models.CharField(verbose_name='Полное имя', max_length=255)

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ('full_name',)
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Publisher(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Издательство'
        verbose_name_plural = 'Издательства'


class Category(models.Model):
    title = models.CharField(verbose_name='Название', max_length=255)

    def get_absolute_url(self):
        return reverse('library:category_book_list', args=(self.id,))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Tag(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255)
    color = models.CharField(verbose_name="Цвет", max_length=20, choices=BACKGROUND_COLORS, default='bgm-gray')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
