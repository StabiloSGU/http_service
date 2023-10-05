from django.db import models

class ImportSettings(models.Model):
    DB = 0
    PANDAS = 1
    STORAGE_METHOD_VARIANTS = [
        (DB, "Database"),
        (PANDAS, "Pandas")
    ]
    name = models.CharField(max_length=200, blank=False, null=False)
    value = models.CharField(max_length=250, blank=False, null=False)

    def __str__(self):
        return f'Import option: {self.name}'
