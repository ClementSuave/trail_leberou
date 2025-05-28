from django import forms

class ChronoForm(forms.ModelForm):
	class Meta:
		model = coureur
		fields = 'dossard'
		widgets = {'heure_arrivee': forms.HiddenInput()}
