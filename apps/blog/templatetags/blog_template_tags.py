from django import template
from django.utils.safestring import mark_safe
from apps.blog.models import Category

register = template.Library()


@register.inclusion_tag(filename='blog/category_sidebar.html',
                        name='include_category_sidebar')
def show_post_categories():
    context = {
        'categories': Category.objects.all()
    }
    return context


@register.simple_tag(takes_context=True)
def get_like_icon(context, post=None):
    template_string = '<span class="uk-margin-small-right" uk-icon="icon:heart;" %s></span>'
    style = ''
    user = context['request'].user
    has_liked = post.likes.filter(user=user).exists() if not user.is_anonymous else False
    if has_liked:
        style = 'style="color: red"'
    return mark_safe(template_string % style)


@register.simple_tag(takes_context=True)
def get_comment_icon(context, post=None):
    template_string = '<span class="uk-margin-small-right uk-margin-small-left" uk-icon="icon:comment;" %s></span>'
    style = ''
    user = context['request'].user
    has_commented = post.comments.filter(author=user).exists() if not user.is_anonymous else False
    if has_commented:
        style = 'style="color: blue"'
    return mark_safe(template_string % style)
