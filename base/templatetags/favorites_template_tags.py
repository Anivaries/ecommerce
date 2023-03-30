from django import template
from ..models import UserProfile


register = template.Library()


@register.filter
def count_favorites(user):
    if user.is_authenticated:
        qs = UserProfile.objects.filter(user=user)
        if qs.exists():
            return qs[0].favorites.count()
    return 0
