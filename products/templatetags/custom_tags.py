from django import template
from products.views import create_review_stars


register = template.Library()


@register.filter(name='ratingstars')
def ratingstars(value):
    """ Filter to display review stars based on value"""
    return create_review_stars(value)
