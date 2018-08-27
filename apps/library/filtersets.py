import django_filters
from django_filters import widgets
from django import forms
from .models import Book, Tag


class BookFilterSet(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='contains', widget=forms.TextInput(attrs={'class': 'uk-input'}))
    description = django_filters.CharFilter(lookup_expr='contains', widget=forms.TextInput(attrs={'class': 'uk-input'}))
    year = django_filters.RangeFilter(widget=widgets.RangeWidget(attrs={'class': 'uk-input'}))
    page_count = django_filters.RangeFilter(widget=widgets.RangeWidget(attrs={'class': 'uk-input'}))
    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all(),
                                                    widget=forms.SelectMultiple(attrs={'class': 'uk-select'}))

    class Meta:
        model = Book
        fields = ('title', 'description', 'year', 'page_count', 'tags',)
