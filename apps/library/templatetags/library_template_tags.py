from django import template
from apps.library.models import Category, Book
from apps.library.forms import BookFilterForm

register = template.Library()


@register.inclusion_tag(filename='library/category_sidebar.html')
def include_library_category_sidebar(current_category=None):
    context = {
        'categories': Category.objects.all(),
        'current_category': current_category,
        'books_count': Book.objects.count(),
        'books_without_category_count': Book.objects.filter(category=None).count()
    }
    return context


@register.inclusion_tag(filename='library/book_filter.html', takes_context=True)
def include_library_book_filter(context):
    book_filter_form = BookFilterForm(data=context['request'].GET)
    print(context['request'].GET)

    context.update({
        'filter_form': book_filter_form,
    })
    return context
