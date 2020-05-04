from django import forms
from django.forms.widgets import TextInput, CheckboxSelectMultiple
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.forms import PasswordResetForm, \
    UserChangeForm, UserCreationForm


class ConnectionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=100, widget=forms.TextInput(
        attrs={"placeholder": "NOM.prenom", "class": "uk-input uk-width-1-2"}))
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(
        attrs={"placeholder": "Mot de passe", "class": "uk-input uk-width-1-2"}))


class CourtCircuitConnectionForm(ConnectionForm):
    username = forms.CharField(
        label="Nom d'utilisateur", max_length=5, required=False)
    username.widget = forms.TextInput(
        attrs={'disabled': 'disabled', 'value': 'court-circuit', 'class': 'uk-input uk-width-1-2'})


class CustomUserChangeForm(UserChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({"class": "uk-input"})
        self.fields['first_name'].widget.attrs.update({"class": "uk-input"})
        self.fields['last_name'].widget.attrs.update({"class": "uk-input"})
        self.fields['email'].widget.attrs.update({"class": "uk-input"})
        self.fields['is_active'].widget.attrs.update({"class": "uk-checkbox"})

    class Meta(UserChangeForm.Meta):
        fields = ['username', 'first_name',
                  'last_name', 'email', 'groups', 'is_active']
        widgets = {
            'groups': CheckboxSelectMultiple(attrs={"class": "uk-list"})
        }


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Update attrs of fields.
        self.fields['username'].widget.attrs.update({"class": "uk-input"})
        self.fields['first_name'].widget.attrs.update({"class": "uk-input"})
        self.fields['last_name'].widget.attrs.update({"class": "uk-input"})
        self.fields['email'].widget.attrs.update({"class": "uk-input"})
        self.fields['password1'].widget.attrs.update({"class": "uk-input"})
        self.fields['password2'].widget.attrs.update({"class": "uk-input"})

    class Meta(UserCreationForm.Meta):
        fields = ['username', 'first_name', 'last_name', 'email', 'groups', 'password1', 'password2']
        widgets = {
            'groups': CheckboxSelectMultiple(attrs={"class": "uk-list", "style": ".uk-list > li > input: "})
        }