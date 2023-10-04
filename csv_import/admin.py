from django.contrib import admin
from csv_import.models import *

admin.site.register(Upload)
admin.site.register(UploadContentsFields)
admin.site.register(UploadContentsFieldValues)
admin.site.register(ImportSettings)