from django import forms

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder': 'Sujet'}),label='')
    message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'placeholder': 'Message'}),label='')
    sender = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'mail'}),label='')