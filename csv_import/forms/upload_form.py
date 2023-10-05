from django import forms
from csv_import.models import *

class UploadForm(forms.ModelForm):
    upload_choice = forms.ChoiceField(choices=ImportSettings.STORAGE_METHOD_VARIANTS)
    class Meta:
        model = Upload
        fields = ['name', 'file']
        widgets = {
            'name' : forms.TextInput(),
        }