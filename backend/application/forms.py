from django.forms import models

from backend.application.models import Product


class ProductForm(models.ModelForm):

    class Meta:
        model = Product
        fields = ('name', 'description')
