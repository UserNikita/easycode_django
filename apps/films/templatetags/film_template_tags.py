from django import template

register = template.Library()


@register.inclusion_tag(filename="films/rating_widget.html", takes_context=True)
def rating_widget(context):
    context["stars"] = range(5)
    return context
