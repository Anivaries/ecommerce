from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile
from django.conf import settings
User = settings.AUTH_USER_MODEL


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        first_name = instance.first_name
        last_name = instance.last_name
        email = instance.email
        # phone_number = instance.phone_number
        UserProfile.objects.create(
            user=instance, first_name=first_name, last_name=last_name, email=email)
