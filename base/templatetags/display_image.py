from django import template
from ..models import Product

register = template.Library()


@register.filter
def add_str(arg1, arg2):
    return str(arg1)+str(arg2)
