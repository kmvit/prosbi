from django.db import models


class ActiveManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super(ActiveManager, self).get_queryset(*args, **kwargs).filter(active=True)