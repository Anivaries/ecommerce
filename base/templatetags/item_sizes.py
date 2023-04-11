from django import template
from ..models import Product, Brand


register = template.Library()


@register.simple_tag(name="item_sizes", takes_context=True)
def item_sizes(context):
    item = context['object']
    items = Product.objects.filter(short_description=item.short_description)
    return items


@register.simple_tag(name="all_brands", takes_context=True)
def all_brands(context):
    brand_qs = Brand.objects.all()
    return brand_qs
