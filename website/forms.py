from django import forms
from .models import Extract

class ExtractChoiceForm(forms.Form):
    file_to_import = forms.ModelChoiceField(
        queryset=Extract.objects.all(),
        label="Choose a csv file to import",
        empty_label="--- Select a file ---"
    )
