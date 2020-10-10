from django.forms import models, TextInput, Textarea, URLInput, CheckboxInput, DateTimeInput, SplitDateTimeField

from django.contrib.admin import widgets

from backend.stats.models import PageAccess


class PageAccessForm(models.ModelForm):
    """ Class for define form display with CreatePageAccess."""
    class Meta:
        model = PageAccess
        fields = '__all__'
        field_classes = {
            "start_date": SplitDateTimeField
        }
        widgets = {
            "name": TextInput(attrs={"class": "uk-input"}),
            "url": URLInput(attrs={"class": "uk-input"}),
            "access": CheckboxInput(attrs={"class": "uk-checkbox"}),
            "raise_exception": CheckboxInput(attrs={"class": "uk-checkbox"}),
            "title": TextInput(attrs={"class": "uk-input"}),
            "content": Textarea(attrs={"class": "uk-textarea"}),
            "start_date": widgets.AdminSplitDateTime()
        }