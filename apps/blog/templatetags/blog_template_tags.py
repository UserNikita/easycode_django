from django import template
from apps.blog.models import Category

register = template.Library()


@register.inclusion_tag(filename='blog/category_sidebar.html',
                        name='include_category_sidebar')
def show_post_categories():
    context = {
        'categories': Category.objects.all()
    }
    return context
