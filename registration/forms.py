from django import forms

from django.contrib.auth.forms import PasswordResetForm

class ConnectionForm(forms.Form):
	username = forms.CharField(label="Nom d'utilisateur", max_length=100, widget=forms.TextInput(attrs={"placeholder":"NOM.prenom","class":"uk-input uk-width-1-2"}))
	password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={"placeholder":"Mot de passe","class":"uk-input uk-width-1-2"}))

class CourtCircuitConnectionForm(ConnectionForm):
	username = forms.CharField(label="Nom d'utilisateur", max_length=5, required=False)
	username.widget = forms.TextInput(attrs={'disabled':'disabled', 'value':'court-circuit', 'class':'uk-input uk-width-1-2'})