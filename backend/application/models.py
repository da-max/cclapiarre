from django.db import models
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User, Permission, Group
from django.contrib.contenttypes.models import ContentType

from ckeditor.fields import RichTextField


class ApplicationImage(models.Model):
    """ ApplicationImage model is use by Application model
    for display images on Command view of each application.

    Fields:
        alt --- CharField, text display in alternative, if image cannot be displayed.
        image --- ImageField, image display on command view.
    """
    alt = models.CharField(verbose_name="Texte alternatif", max_length=60,
                           help_text="Texte affiché si l’image ne peut pas être affichée.")
    image = models.ImageField(verbose_name="Image a affiché")

    def __str__(self):
        return self.alt

    class Meta:
        verbose_name = "Image d’application"


class Application(models.Model):
    """ Application model, this model is use by many of the following models
    because it describes the core of the created application.

    Fields:
        name --- CharField,
        description --- RichTextField for better styling.
    """
    name = models.CharField(
        verbose_name="Nom de l’application", max_length=60, unique=True)
    slug = models.SlugField(verbose_name="Chemin menant à l’application",
                            unique=True, help_text="Ce champs définira l’URL menant à l’application.")
    description = RichTextField(verbose_name="Description de l’application",
                                help_text="Cette description s’affichera sur l’entête de la page permettant de commander.")
    images = models.ManyToManyField('ApplicationImage', related_name='images')
    table = models.BooleanField(verbose_name="Mode d’affichage de l’application",
                                help_text="Défini si l’application doit être affichée sous forme de tableau \
                                    (convient pour les applications dont les produits n’ont pas d’options).", default=False)
    admins = models.ManyToManyField(User, related_name='admin_application')
    members = models.ManyToManyField(User, related_name='member_application')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Application"


class Option(models.Model):
    """ Option model is use by Product Model for define option for product.

    Fields:
        name --- CharField
    """
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, verbose_name='Application de l’option')
    name = models.CharField(verbose_name='Nom de l’option', max_length=60)

    class Meta:
        verbose_name = "Option"


class Weight(models.Model):
    """ Weight model define all weights and price for all products.



    """
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, verbose_name="Application des poids", related_name='weights')
    weight = models.FloatField(verbose_name="Poids du produit")
    unit = models.CharField(verbose_name="Unité du poids", max_length=20)
    price = models.FloatField(verbose_name="Prix du produit")

    def __str__(self):
        return '{} {} pour {}'.format(self.weight, self.unit, self.price)

    class Meta:
        verbose_name = "Poids"
        verbose_name_plural = verbose_name


class Product(models.Model):
    """ Product model define all products for all applications.


    Fields:
        name --- CharField, name of product
        application --- ForeignKey to Application model for define to what application this product is use.
        weights ---  ManyToManyField to Weight Model to define which weights are available for this product
        description --- RichTextField to describe the product.
        display --- BooleanField to define if this product is display and orderable.
        options --- ManyToManyField to define options for this product.
        maximum --- IntergerField for define maximum amount orderable by member.
        maximum_all --- IntergerField for define maximum amount orderable by all members.
    """
    name = models.CharField(verbose_name="Nom du produit", max_length=60)
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, verbose_name="Application du produit", related_name="products")
    weights = models.ManyToManyField(
        Weight, related_name='weights', verbose_name="Poids disponible pour ce produit")
    description = RichTextField(verbose_name="Description du produit")
    display = models.BooleanField(
        verbose_name="Afficher le produit sur le tableau des commandes", default=True)
    image = models.ImageField(verbose_name="Image de présentation du produit",
                              help_text="Cette image s’affichera sur la carte de présentation du produit.", upload_to='application/products')
    options = models.ManyToManyField(
        Option, verbose_name="Options disponible pour ce produit", blank=True)
    maximum = models.IntegerField(
        verbose_name="Quantité maximum commandable par adhérent", default=100)
    maximum_all = models.IntegerField(verbose_name="Quantité maximum disponible",
                                      help_text="Cette nombre représente la quantité maximum commandable par tout les adhérents.", default=1000)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Produit'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product, through='Amount', through_fields=(
        'order', 'product'), verbose_name="Produits de la commande")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Commande'


class Amount(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Produit commandé")
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, verbose_name="Commande associé")
    amount = models.FloatField(verbose_name="Quantité commandée")
    option = models.ForeignKey(
        Option, on_delete=models.CASCADE, verbose_name="Option du produit", blank=True, null=True)
    weight = models.ForeignKey(
        Weight, on_delete=models.CASCADE, verbose_name="Poids du produit")

    class Meta:
        verbose_name = "Quantité"
