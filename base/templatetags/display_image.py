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


@register.simple_tag(name="perfume_highlights", takes_context=True)
def carousel(context):
    product = context['object']
    perfume_highlights = os.listdir(os.path.join(settings.BASE_DIR,
                                                 'static/base/static/catalog/highlights'))
    lis = [str(a) for a in product.highlights.all() if str(
        a) in str(perfume_highlights)]
    return lis
