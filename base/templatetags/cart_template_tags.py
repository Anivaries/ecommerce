from django import template
from ..models import Order
register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False,)
        if qs.exists():
            return qs[0].items.count()
    return 0


@register.simple_tag(name="show_cart_items", takes_context=True)
def show_cart_items(context):
    user = context['request'].user
    try:
        if user.is_authenticated:
            qs = Order.objects.get(user=user, ordered=False)
            if qs.items.exists():
                return qs.items.all()
    except Order.DoesNotExist:
        return None


@register.simple_tag(name="price_for_all", takes_context=True)
def price_for_all(context):
    user = context['request'].user
    try:
        if user.is_authenticated:
            order = Order.objects.get(user=user, ordered=False)
            return order.get_total_price()
    except Order.DoesNotExist:
        return 0
