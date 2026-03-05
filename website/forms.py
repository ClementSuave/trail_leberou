from django import forms
from django.forms import ModelForm
from .models import Extract, Benevole

class ExtractChoiceForm(forms.Form):
    file_to_import = forms.ModelChoiceField(
        queryset=Extract.objects.all(),
        label="Choose a csv file to import",
        empty_label="--- Select a file ---"
    )

class ResultUpdateForm(forms.Form):
    dossard = forms.IntegerField(label="Numéro de Dossard")

class BenevoleForm(ModelForm):
    class Meta:
        model = Benevole
        fields = ['nom', 'prenom', 'adresse','CP','ville','email', 'telephone']
        widgets = {
            'nom': forms.TextInput(attrs={'placeholder': 'Votre nom'}),
            'prenom': forms.TextInput(attrs={'placeholder': 'Votre prénom'}),
            'adresse': forms.TextInput(attrs={'placeholder': 'Adresse'}),
            'CP': forms.TextInput(attrs={'placeholder': 'CP'}),
            'ville': forms.TextInput(attrs={'placeholder': 'Ville'}),
            'email': forms.EmailInput(attrs={'placeholder': 'nom@exemple.com'}),
            'telephone': forms.TextInput(attrs={'placeholder': '06 00 00 00 00'}),
        }
