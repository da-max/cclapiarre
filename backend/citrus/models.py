from random import random
from django.db.models import Model, ForeignKey, ManyToManyField, CASCADE
from django.db.models.fields import CharField, FloatField, IntegerField, BooleanField

from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class CitrusProduct(Model):
    name = CharField(max_length=255, verbose_name="Nom du produit")
    description = RichTextField(
        blank=True, verbose_name="Description du produit", help_text="Ce champ est optionnel.")
    weight = FloatField(default=10, verbose_name="Poids du produit",
                        help_text="Mettre 1 si ce produit n'est pas vendu au poids.")
    price = FloatField(default=1, verbose_name="Prix du produit")
    display = BooleanField(verbose_name="Afficher le produit")
    maybe_not_available = BooleanField(verbose_name="Produit peut être non disponible", default=False,
                                       help_text="Cocher cette case si le produit peut ne pas être disponible.")
    step = FloatField(default=1, verbose_name="Pas d'augmentation du produit")
    maximum = IntegerField(
        default=100, verbose_name="Quantité maximal commandable par commande")

    class Meta:
        verbose_name = "Produit"

    def __str__(self):
        return self.name

    def get_total(self):
        total = float()
        amounts = CitrusOrder.objects.filter(product=self)
        for amount in amounts:
            total += amount.amount
        return total


class CitrusOrder(Model):
    number = IntegerField(default=int(random() * 1000),
                          help_text="Merci de laisser la valeur par défaut.")
    user = ForeignKey(User, on_delete=CASCADE, related_name="utilisateur")
    product = ManyToManyField(
        CitrusProduct, through='CitrusAmount', related_name='commands')
    send_mail = BooleanField(verbose_name='Envoyer un mail', default=True,
                             help_text="Décocher cette case afin qu'aucun mail ne soit envoyé à l'utilisateur \
                             lors de sa commande (ou de la modification de sa commande.")

    class Meta:
        verbose_name = "Commande"

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = float()
        amounts = CitrusOrder.objects.filter(command=self)
        for amount in amounts:
            total += amount.product.price * amount.amount

        return total


class CitrusAmount(Model):
    product = ForeignKey(CitrusProduct, on_delete=CASCADE, related_name="amounts")
    order = ForeignKey(CitrusOrder, on_delete=CASCADE, related_name="amounts")
    amount = FloatField(verbose_name="Quantité commandé")

    class Meta:
        verbose_name = "Quantité"

    def __str__(self):
        return "{} faites par {} commander {}".format(self.product.name, self.order.user.username, self.amount)

    def get_total_product(self, product):
        total = int()
        products = self.objects.filter(product=product)
        for product in products:
            total += product.amount
        return total

    def get_total_user(self, order_id):
        total = float()
        order = self.objects.filter(order_id=order_id)
        for c in order:
            total += c.product.price * c.amount
        return total
