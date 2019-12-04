from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from society.models import Profile


@receiver(post_save, sender=get_user_model())
def profile_handler(sender, instance, created, **kwargs):
    if created and sender.profile is None:
        Profile.objects.create(user_id=sender)
