from django.template import Library

register = Library()


@register.filter(name='split_get_first')
def split_get_first(value, sep):
    return value.split(sep)[0]
