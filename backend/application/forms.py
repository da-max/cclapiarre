from django.forms import models

from backend.application.models import Application, Product


class ProductForm(models.ModelForm):

    class Meta:
        model = Product
        fields = ('name', 'description')


class ApplicationForm(models.ModelForm):

    class Meta:
        model = Application
        fields = ('name', 'description')
