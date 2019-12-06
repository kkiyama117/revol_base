from django.db import models

from society.queryset import LogicalDeleteQuerySet


class LogicalDeleteManager(models.Manager):
    _queryset_class = LogicalDeleteQuerySet

    def get_queryset(self):
        if self.model:
            return (self._queryset_class(self.model, using=self._db)
                    .filter(is_deleted=False))

    def all_with_deleted(self):
        if self.model:
            return super(LogicalDeleteManager, self).get_queryset()

    def deleted(self):
        if self.model:
            return (super(LogicalDeleteManager, self)
                    .get_queryset()
                    .filter(is_deleted=True))

    def get(self, *args, **kwargs):
        return self.all_with_deleted().get(*args, **kwargs)

    def filter(self, *args, **kwargs):
        if "pk" in kwargs:
            return self.all_with_deleted().filter(*args, **kwargs)

        return self.get_queryset().filter(*args, **kwargs)