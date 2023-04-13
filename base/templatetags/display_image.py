from django import template
from ..models import Product
import os
from django.conf import settings

register = template.Library()


@register.filter
def add_str(arg1, arg2):
    return str(arg1)+str(arg2)


@register.simple_tag(name="carousel")
def carousel():
    c_base = os.listdir(os.path.join(settings.BASE_DIR,
                        'static/base/static/carousel'))
    return c_base
