from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

from society.models import Profile


def profile_handler(sender, instance, created, **kwargs):
    if created and sender.profile is None:
        Profile.objects.create(user_id=sender)


post_save.connect(profile_handler, sender=get_user_model(),
                  dispatch_uid="my_unique_identifier")
