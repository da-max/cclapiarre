from django.forms import models, TextInput, NumberInput, CheckboxInput, Textarea, Select
from django.forms.widgets import Select, CheckboxSelectMultiple

from ckeditor.widgets import CKEditorWidget

from backend.coffee.models import Coffee, Origin

class CoffeeForm(models.ModelForm):
    """ Class for create or update a coffee product."""

    class Meta:
        model = Coffee
        fields = "__all__"
        widgets = {
            'origin': Select({'class':'uk-select'}),
            'farm_coop': TextInput(attrs={'class':'uk-input'}),
            'region': TextInput(attrs={'class':'uk-input'}),
            "description": Textarea(attrs={"class" : 'uk-textarea'}),
            'process': TextInput(attrs={'class':'uk-input'}),
            'variety': TextInput(attrs={'class': 'uk-input'}),
            'two_hundred_gram_price': NumberInput(attrs={'class':'uk-input'}),
            'kilogram_price': NumberInput(attrs={'class':'uk-input'}),
            'display': CheckboxInput(attrs={'class':'uk-checkbox'}),
            'maximum': NumberInput(attrs={'class':'uk-input'}),
            'available_type': CheckboxSelectMultiple(attrs={'class': 'uk-list uk-list-bullet'})
        }
        labels = {
            'origin': "Origine du café",
            'available_type': "Type de mouture disponible"

        }
        

class OriginForm(models.ModelForm):
    """ Class for create or update an origin."""

    class Meta:
        model = Origin
        fields = "__all__"
        widgets = {
            'name' : TextInput(attrs={'class':'uk-input'})
        }