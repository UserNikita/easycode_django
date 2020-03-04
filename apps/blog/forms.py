from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Post


class PostFormAdmin(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'text': SummernoteWidget(),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'category', 'slug', 'description', 'text', 'tags', 'draft',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'uk-input uk-form-width-large'}),
            'category': forms.Select(attrs={'class': 'uk-select uk-form-width-large'}),
            'slug': forms.TextInput(attrs={'class': 'uk-input uk-form-width-large'}),
            'description': forms.Textarea(attrs={'rows': 5, 'class': 'uk-input uk-form-width-large'}),
            'text': SummernoteWidget(),
            'tags': forms.SelectMultiple(attrs={'class': 'uk-select uk-form-width-large'}),
            'draft': forms.CheckboxInput(attrs={'class': 'uk-checkbox'}),
        }
