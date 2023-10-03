from django import forms
from csv_import.models import *

class UploadForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ['name', 'file']
        widgets = {
            'name' : forms.TextInput(),
        }