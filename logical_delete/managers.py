from django.db import models

from logical_delete.queryset import LogicalDeleteQuerySet


class LogicalDeleteManager(models.Manager):
    _queryset_class = LogicalDeleteQuerySet

    def get_queryset(self):
        if self.model:
            return (self._queryset_class(self.model, using=self._db)
                    .filter(deleted_at__isnull=True))

    def all_with_deleted(self):
        if self.model:
            return super(LogicalDeleteManager, self).get_queryset()

    def deleted_set(self):
        if self.model:
            return (super(LogicalDeleteManager, self)
                    .get_queryset()
                    .filter(deleted_at__isnull=False))

    def get(self, *args, **kwargs):
        if 'pk' in kwargs:
            return self.all_with_deleted().get(*args, **kwargs)
        return self._get_self_queryset().get(*args, **kwargs)

    def filter(self, *args, **kwargs):
        if "pk" in kwargs:
            return self.all_with_deleted().filter(*args, **kwargs)

        return self.get_queryset().filter(*args, **kwargs)
