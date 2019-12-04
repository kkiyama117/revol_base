from django.db import models


class Auth(models.Model):
    # user = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        pass


class Omniauth(Auth):
    class Meta:
        pass
