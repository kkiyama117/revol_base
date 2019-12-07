from django.db.models.query import QuerySet


class LogicalDeleteQuerySet(QuerySet):
    def delete(self):
        assert self.query.can_filter(), \
            "Cannot use 'limit' or 'offset' with delete."

        # Override したDeleteで論理削除していく
        self.all().delete()

        self._result_cache = None

    def hard_delete(self):
        return super(LogicalDeleteQuerySet, self).delete()

    def recover(self):
        assert self.query.can_filter(), \
            "Cannot use 'limit' or 'offset' with recover."
        for i in self.all():
            i.recover()
        self._result_cache = None

    delete.alters_data = True
