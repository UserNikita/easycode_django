from django import template
from apps.library.models import Book, Tag
from apps.library.forms import BookFilterForm

register = template.Library()


@register.inclusion_tag(filename='library/main_sidebar.html')
def include_library_main_sidebar():
    context = {
        'tags': Tag.objects.all(),
        'books_count': Book.objects.count(),
    }
    return context


@register.inclusion_tag(filename='library/book_filter.html', takes_context=True)
def include_library_book_filter(context):
    book_filter_form = BookFilterForm(data=context['request'].GET)

    context.update({
        'filter_form': book_filter_form,
    })
    return context
