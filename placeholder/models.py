from django.db import models


# Create your models here.

class Place(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('Place',
                               related_query_name="%(app_label)s_%(class)ss",
                               on_delete=models.SET_NULL, null=True,
                               blank=True)
    latitude = models.DecimalField(u'緯度', max_digits=9, decimal_places=6,
                                   default=0)
    longitude = models.DecimalField(u'経度', max_digits=9, decimal_places=6,
                                    default=0)

    class Meta:
        abstract = True


class Building(Place):
    pass