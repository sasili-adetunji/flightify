from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
import datetime
from django.utils import timezone
from django.db.models.query import QuerySet

User = get_user_model()

class SoftDeletionQuerySet(QuerySet):
    def delete(self):
        return super(SoftDeletionQuerySet, self).update(
            deleted_at=datetime.datetime.now()
        )

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)


class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class SoftDeletionModel(models.Model):
    deleted_at = models.DateTimeField(blank=True, null=True)
    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = datetime.datetime.now()
        self.save()

    def hard_delete(self):
        super(SoftDeletionModel, self).delete()


class File(SoftDeletionModel):
    """ File model definition """

    name = models.CharField(max_length=255, verbose_name="Name")
    type = models.CharField(max_length=255, verbose_name="MIME Type")
    s3_key = models.TextField(
        null=True, blank=True,
        verbose_name="S3 Key"
    )
    uploader = models.ForeignKey(
        User,
        related_name="files_uploaded",
        on_delete=models.PROTECT
    )
    description = models.TextField(
        null=True, blank=True,
        verbose_name="Description"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated At'
    )
