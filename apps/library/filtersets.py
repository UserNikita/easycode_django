import django_filters
from django_filters import widgets
from django import forms
from .models import Book, Tag, Publisher, Author


class BookFilterSet(django_filters.FilterSet):
    title = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'uk-input'}))
    description = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'uk-input'}))
    year = django_filters.RangeFilter(
        widget=widgets.RangeWidget(attrs={'class': 'uk-input'}))
    page_count = django_filters.RangeFilter(
        widget=widgets.RangeWidget(attrs={'class': 'uk-input'}))
    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'uk-select'}))
    publishers = django_filters.ModelMultipleChoiceFilter(
        queryset=Publisher.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'uk-select'}))
    authors = django_filters.ModelMultipleChoiceFilter(
        queryset=Author.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'uk-select'}))

    class Meta:
        model = Book
        fields = ('title', 'publishers', 'authors', 'description', 'year', 'page_count', 'tags',)
