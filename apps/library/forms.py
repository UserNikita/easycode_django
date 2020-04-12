from django import forms
from django.forms import inlineformset_factory
from django_summernote.widgets import SummernoteWidget
from .models import Book, Author, Publisher, Tag


class BookForm(forms.ModelForm):
    authors_list = forms.CharField(label="Список авторов", help_text="Введите авторов через запятую", required=False,
                                   widget=forms.TextInput(attrs={'class': 'uk-input uk-form-width-large'}))

    def save(self, commit=True):
        book = super().save(commit=commit)
        # Добавление авторов перечисленных в текстовом поле через запятую
        authors_list = self.cleaned_data.get('authors_list', '').split(',')
        authors_list = filter(None, [author.strip() for author in authors_list])
        for author_fullname in authors_list:
            author = Author.objects.get_or_create(full_name=author_fullname)[0]
            book.authors.add(author)
        return book

    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'uk-input uk-form-width-large'}),
            'description': SummernoteWidget(),
            'year': forms.TextInput(attrs={'class': 'uk-input uk-form-width-large'}),
            'authors': forms.SelectMultiple({'class': 'uk-select uk-form-width-large'}),
            'publishers': forms.SelectMultiple({'class': 'uk-select uk-form-width-large'}),
            'category': forms.Select({'class': 'uk-select uk-form-width-large'}),
            'tags': forms.SelectMultiple({'class': 'uk-select uk-form-width-large'}),
            'page_count': forms.NumberInput({'class': 'uk-input uk-form-width-large'}),
            'url': forms.URLInput({'class': 'uk-input uk-form-width-large'}),
            'size': forms.NumberInput({'class': 'uk-input uk-form-width-large'}),
            'format': forms.Select({'class': 'uk-select uk-form-width-large'}),
        }


class BookFilterForm(forms.Form):
    author_id = forms.MultipleChoiceField(label='Автор')
    publisher_id = forms.MultipleChoiceField(label='Издательство')
    tag_id = forms.MultipleChoiceField(label='Тэг', widget=forms.CheckboxSelectMultiple())

    def __init__(self, **kwargs):
        super(BookFilterForm, self).__init__(**kwargs)
        for field_name in self.fields:  # Делаем все поля необязательными
            self.fields[field_name].required = False
        self.fields['author_id'].choices = [(x.id, x.full_name) for x in Author.objects.all()]
        self.fields['publisher_id'].choices = [(x.id, x.name) for x in Publisher.objects.all()]
        self.fields['tag_id'].choices = [(x.id, x.name) for x in Tag.objects.all()]


class BookAdminForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'description': SummernoteWidget(),
        }
