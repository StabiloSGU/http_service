from django.db import models
from csv_import.models import Upload

class UploadContentsFields(models.Model):
    file = models.ForeignKey(
        to=Upload,
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=100,
        blank=False,
        null=False
    )


class UploadContentsFieldValues(models.Model):
    field = models.ForeignKey(
        to=UploadContentsFields,
        on_delete=models.CASCADE
    )
    row_num = models.IntegerField(
        blank=False,
        null=False
    )
    value = models.CharField(
        max_length=255,
        blank=True,
        null=False
    )