from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse
from django.templatetags.static import static
from django.utils.safestring import mark_safe
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io
import os


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
    cover = models.ImageField(verbose_name="Обложка", blank=True, upload_to='library/covers')
    cover_thumbnail = models.ImageField(verbose_name="Превью", blank=True, upload_to='library/thumbnails')
    authors = models.ManyToManyField(verbose_name="Авторы", to='Author', blank=True)
    publishers = models.ManyToManyField(verbose_name="Издательства", to='Publisher')
    year = models.PositiveIntegerField(verbose_name="Год издания")
    tags = models.ManyToManyField(verbose_name="Теги", to='Tag', blank=True)
    page_count = models.PositiveSmallIntegerField(verbose_name="Количество страниц", default=0)
    draft = models.BooleanField(verbose_name="Черновик", default=False)
    created_date = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    changed_date = models.DateTimeField(verbose_name="Дата последнего изменения", auto_now=True)
    url = models.URLField(verbose_name='Ссылка для скачивания')
    size = models.FloatField(verbose_name='Размер файла', help_text='Условный размер файла в мегабайтах')
    format = models.PositiveSmallIntegerField(verbose_name='Формат файла', choices=FILE_FORMATS, default=0)

    likes = GenericRelation(to='personal_area.Like', related_query_name='books')
    comments = GenericRelation(to='personal_area.Comment', related_query_name='books')

    def create_thumbnail(self):
        """Метод создания миниатюрной обложки для книги"""
        if not self.cover:  # Если обложки нет, то и создавать миниатюру не нужно
            return

        # Если миниатюра уже была создана ранее, то её необходимо удалить
        old_file = self.cover_thumbnail
        if old_file and os.path.isfile(old_file.path):
            os.remove(old_file.path)

        image = Image.open(io.BytesIO(self.cover.read()))
        image.thumbnail(size=(256, image.height), resample=Image.ANTIALIAS)
        temp_handle = io.BytesIO()
        image.save(temp_handle, format='png')
        temp_handle.seek(0)
        suf = SimpleUploadedFile(os.path.split(self.cover.name)[-1], temp_handle.read(), content_type='image/png')
        file_name = '{0}.png'.format(os.path.splitext(suf.name)[0])
        self.cover_thumbnail.save(name=file_name, content=suf, save=False)
        temp_handle.close()

    def save(self, *args, **kwargs):
        self.create_thumbnail()
        super(Book, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('library:book_detail', args=(self.id,))

    def get_cover_url(self):
        if self.cover:
            return self.cover.url
        return static('img/missing_book_cover.jpg')

    def get_cover_thumbnail_url(self):
        if self.cover_thumbnail:
            return self.cover_thumbnail.url
        return static('img/missing_book_cover.jpg')

    def get_cover(self):
        img_html_tag = '<img src="%s" width="50px">' % self.get_cover_thumbnail_url()
        return mark_safe(img_html_tag)

    get_cover.short_description = "Обложка"

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-id',)
        verbose_name = "Книга"
        verbose_name_plural = "Книги"


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


class Tag(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255)
    color = models.CharField(verbose_name="Цвет", max_length=20, choices=BACKGROUND_COLORS, default='bgm-gray')

    def get_absolute_url(self):
        return reverse('library:tag_book_list', args=(self.id,))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
