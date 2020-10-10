from django.forms import models

from application.models import Product


class ProductForm(models.ModelForm):

    class Meta:
        model = Product
        fields = ('name', 'description')
