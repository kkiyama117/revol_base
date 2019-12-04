from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.

class Society(models.Model):
    name = models.CharField(max_length=30, blank=False)
    leader = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Group(models.Model):
    pass


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)
