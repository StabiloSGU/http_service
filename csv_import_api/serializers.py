from rest_framework import serializers
from csv_import.models import *


class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = ('pk', 'name', 'file')
