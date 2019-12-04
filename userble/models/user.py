from django.contrib.auth import get_user_model
from django.db import models

from django.utils.translation import gettext_lazy as _


class Auth(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    email = models.EmailField(_('email address'), blank=True, unique=True)

    class Meta:
        pass


class Omniauth(Auth):
    class Meta:
        pass
