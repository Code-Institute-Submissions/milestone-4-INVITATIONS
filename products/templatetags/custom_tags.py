from django import template

register = template.Library()


@register.filter(name='ratingstars')
def ratingstars(value):
    return 'Hello World!'
