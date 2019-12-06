from logging import getLogger

from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from society.managers import LogicalDeleteManager

logger = getLogger(__name__)


class LogicalDeleteModel(models.Model):
    objects = LogicalDeleteManager()
    #: 削除されたかどうか
    is_deleted = models.BooleanField(default=False)
    #: 削除日時
    deleted_at = models.DateTimeField(null=True, blank=True)

    def delete(self, using=None, **kwargs):
        if self.is_deleted:
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
            self.is_deleted = True
            self.deleted_at = now()
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
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    class Meta:
        abstract = True


class Society(models.Model):
    name = models.CharField(max_length=30, blank=False)

    # leader = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Group(models.Model):
    pass


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)
