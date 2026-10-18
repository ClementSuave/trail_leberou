from django import forms
from django.forms import ModelForm
from .models import Extract, Benevole, Course

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

TEMPLATE_CHOICES = [
    ('emails/mail_precourse.html', 'Avant-Course (Info pratiques)'),
    ('emails/mail_remerciements.html', 'After course'),
]

class SendEmailForm(forms.Form):
    template_path = forms.ChoiceField(
        choices=TEMPLATE_CHOICES,
        label="Modèle de mail"
    )
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        required=False,
        empty_label="--- Toutes les épreuves ---",
        label="Épreuve visée"
    )
    sujet = forms.CharField(
        max_length=200,
        label="Objet de l'email",
        initial="Trail du Lébérou",
        widget=forms.TextInput(attrs={'style': 'width: 100%; max-width: 600px;'})
    )