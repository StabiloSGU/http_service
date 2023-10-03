import os
from django.db import models
from django.dispatch import receiver

class Upload(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to="csv_import/uploads/")

    def __str__(self):
        return f"Uploaded file: {self.name}"

@receiver(models.signals.post_delete, sender=Upload)
def delete_csv_file(sender, instance, *args, **kwargs):
    if os.path.isfile(instance.file.path):
        os.remove(instance.file.path)