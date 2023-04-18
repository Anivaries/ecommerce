from django import template
from ..models import Product, Brand
import datetime
from django.db.models import Q
register = template.Library()


@register.simple_tag(name="item_sizes", takes_context=True)
def item_sizes(context):
    item = context['object']
    items = Product.objects.filter(short_description=item.short_description)
    return items


@register.simple_tag(name="all_brands_p", takes_context=True)
def all_brands_p(context):
    brand_qs = Brand.objects.exclude(~Q(product__category="P"))
    return brand_qs


@register.simple_tag(name="all_brands_s", takes_context=True)
def all_brands_s(context):
    brand_qs = Brand.objects.exclude(~Q(product__category="S"))
    return brand_qs


@register.filter
def date_today():
    date = datetime.datetime.now()
    return date
