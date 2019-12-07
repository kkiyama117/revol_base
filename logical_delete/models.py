import datetime
from logging import getLogger

from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from django.utils import timezone

from logical_delete.managers import LogicalDeleteManager

logger = getLogger(__name__)


class LogicalDeleteModel(models.Model):
    def __init__(self, *args, **kwargs):
        super(LogicalDeleteModel, self).__init__(*args, **kwargs)

    objects = LogicalDeleteManager()
    #: 削除日時
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)

    @property
    def deleted(self):
        return self.deleted_at is not None

    @deleted.setter
    def deleted(self, d):
        """Called via the admin interface
         (if user checks the "deleted" checkbox)"""
        if d and not self.deleted_at:
            self.deleted_at = timezone.now()
        elif not d and self.deleted_at:
            self.deleted_at = None

    def delete(self, using=None, **kwargs):
        if self.deleted:
            logger.debug("Hard deleting skipped %s: %s", type(self), self)
        else:
            logger.debug("Soft deleting %s: %s", type(self), self)

            # Simulate Model._meta.get_all_related_objects()
            all_related_objects = [
                f for f in self._meta.get_fields()
                if (f.one_to_many or f.one_to_one)
                and f.auto_created and not f.concrete
            ]
            # このモデルのリレーションのリストを取得
            related_objects = [
                relation.get_accessor_name()
                for relation in all_related_objects
            ]

            for related_object in related_objects:
                # それぞれのリレーションについてすべてのオブジェクトを取得
                objects = getattr(self, related_object).all()

                for obj in objects:
                    # 論理削除に対応しているかどうかで処理を分ける場合
                    if issubclass(obj.__class__, LogicalDeleteModel):
                        obj.delete()
                    else:
                        pass

                    # 論理削除に対応しているかの如何を問わず, 関係先のオブジェクトを削除
                    # obj.delete()

            # 論理削除
            self.deleted_at = datetime.datetime.now()
            self.save()

    def recover(self):
        logger.debug("Recovering %s: %s", type(self), self)

        # Simulate Model._meta.get_all_related_objects()
        all_related_objects = [
            f for f in self._meta.get_fields()
            if (f.one_to_many or f.one_to_one)
            and f.auto_created and not f.concrete
        ]
        # このモデルのリレーションのリストを取得
        related_objects = [
            relation.get_accessor_name()
            for relation in all_related_objects
        ]

        for related_object in related_objects:
            # それぞれのリレーションについてすべてのオブジェクトを取得
            objects = getattr(self, related_object).all()

            for obj in objects:
                # 論理削除に対応しているかどうかで処理を分ける場合
                if issubclass(obj.__class__, LogicalDeleteModel):
                    obj.recover()
                else:
                    pass

        # 復旧
        self.deleted_at = None
        self.save()

    def hard_delete(self):
        super(LogicalDeleteModel, self).delete()

    class Meta:
        abstract = True
