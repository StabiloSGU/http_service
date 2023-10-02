from django.db import models

class Upload(models.Model):
    name = models.CharField(max_length=100)
    #yes this is a bad design but should wok for test case purposes
    file = models.FileField(upload_to="csv_import/uploads/")

    def __str__(self):
        return f"Uploaded file: {self.name}"
