from random import random
from django.db.models import Model, ForeignKey, ManyToManyField, CASCADE
from django.db.models.fields import CharField, IntegerField, FloatField, BooleanField

from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from phonenumber_field.modelfields import PhoneNumberField


class Command(Model):
    number = IntegerField(default=int(random()*1000),
                          help_text="Merci de laissé la valeur par défaut.")
    name = CharField(verbose_name="Nom", max_length=100)
    first_name = CharField(verbose_name="Prénom", max_length=100)
    email = CharField(verbose_name="Email", max_length=100)
    phone_number = PhoneNumberField(verbose_name="Numéro de téléphone")

    def __str__(self):
        return "Commande faite par {} {}".format(self.name, self.first_name)

    class Meta:
        verbose_name = "Commande"
        abstract = True


class Origin(Model):
    """Origin class for listing all origin of coffee.
    Its take only on field : name with 255 caracteres max.

    Attributes
    ----------
    name : str
        Fields for mark name of origin country of coffee.
    """

    name = CharField(max_length=255, verbose_name="Nom du pays d'origine")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Origine"


class Type(Model):
    """ Type of coffee. This class listing all type of coffee available for all coffee.
    It as well use in  Quantity class for indicate whath type user has command.

    Attributes
    ----------
    name : str 
        Name of type of coffee.
    """
    name = CharField(max_length=255, verbose_name="Nom du type de café")

    def __str__(self):
        """ Method for better display. return name of type. """

        return self.name

    class Meta:
        """ Meta class for display name of class in french. """

        verbose_name = "Type de café"


class Coffee(Model):
    """ Class coffee for listing all coffee available. 
    It take lot of informations.

    Attributes
    ----------
    origin : int
        ForeignKey for Origin model, it's origin of coffee.
    farm_coop : str
        Farm or Cooperative where coffee does come. It's CharField with 255 caracteres max.
    region : str
        Region where it does come (it is also name of coffee). It's CharField with 255 caracteres max.
    process : str
        Process of coffee making. It's CharField with 255 caracteres max.
    variety : str
        Variety of coffee. It's CharField with 255 caractere max.
    two_hundred_gram_price : float
        Price for 200 gram of coffee. It's FloatField, with default value : 1
    kilagram_price : float
        Price for 1KG. It's FloatField, with default value : 1
    display : bool
        If it's True, coffee is display in table of command. It's BooleanField with default True.
    maximun : int 
        Maximun of coffee command by on user. It's IntergerField by 100 default
    available_type : [int]
        Listing of type available for this coffee. ManyToManyField for Type model.
    """
    origin = ForeignKey(Origin, on_delete=CASCADE)
    farm_coop = CharField(max_length=200, verbose_name="Ferme/Coopérative")
    region = CharField(max_length=200, verbose_name="Région du café")
    description = RichTextField(
        blank=True, verbose_name="Description du café", help_text="Ce champ n'est pas obligatoire.")
    process = CharField(
        max_length=200, verbose_name="Procédé de fabrication du café")
    variety = CharField(max_length=200, verbose_name="Variété du café")
    two_hundred_gram_price = FloatField(
        default=1, verbose_name="Prix du produit pour 200 cents grammes")
    kilogram_price = FloatField(
        default=1, verbose_name="Prix du produit au kilo")
    display = BooleanField(default=True, verbose_name="Afficher le café",
                           help_text="Cocher cette case pour que le café soit affiché sur le tableau de la commande.")
    maximum = IntegerField(
        default=100, verbose_name="Quantité maximal commandable par utilisateur")
    available_type = ManyToManyField(Type)

    def __str__(self):
        """ Display origin name and price. """
        return "Café de {}, vendu pour un prix de {} le kilo.".format(self.origin.name, self.kilogram_price)

    class Meta:
        """ Dsiplay name of model in french. """
        verbose_name = "Café"
        verbose_name_plural = "Cafés"


class Order(Model):
    """
    Order model define order for coffee. 

    Attributes
    ----------
    user : int
        ForeignKey to User model.
    coffee : [int]
        ManyToMany to Coffee through Amount model.

    Methods
    -------
    get_price() -> float:
        Method for get price of order.
    """
    user = ForeignKey(User, on_delete=CASCADE, related_name="coffee_order")
    coffee = ManyToManyField(Coffee, through="Amount",
                             through_fields=('order', 'coffee'))

    class Meta:
        verbose_name = 'Commande de café'
        permissions = [
            ('can_command', "Can command coffee"),
        ]

    def get_price(self) -> float:
        """ 
        This function calulate total price for one commande and return this number.

        Returns
        -------
        float : price for this amount.
        """
        amounts = Amount.objects.filter(order=self)

        total_price = float()

        for amount in amounts:

            if amount.weight == 200:
                total_price += amount.amount * amount.coffee.two_hundred_gram_price

            elif amount.weight == 1000:
                total_price += amount.amount * amount.coffee.kilogram_price

        return round(total_price, 3)


class Amount(Model):
    """
    Amount model is use by ManyToMany field coffee in Order model.

    Attributes
    ----------
    coffee : int
        ForeignKey to Coffee model.
    order : int
        ForeignKey to Order model.
    amount : int
        amount of product.
    weight : int
        weight of product order, 200 or 1000.
    sort : int
        ForeignKey to Type model for define witch type is selected.

    Methods
    -------
    get_price() -> float:
        Method for get price for an amount.
    """
    coffee = ForeignKey(Coffee, on_delete=CASCADE,
                        related_name="amounts")
    order = ForeignKey(Order, on_delete=CASCADE,
                       related_name="amounts")
    amount = IntegerField(verbose_name="Quantité commandé")
    weight = IntegerField(verbose_name="Poids commandé", help_text="200 ou 1000 grammes.", choices=(
        (200, '200 grammes'), (1000, '1 kilogramme')))
    sort = ForeignKey(Type, on_delete=CASCADE, related_name="type")

    def __str__(self):
        return '{} a commandé {} (bocaux de {}) du café {} avec un grain "{}"'.format(self.order, self.amount, self.weight, self.coffee.region, self.sort.name)

    class Meta:
        verbose_name = "Quantité"

    def get_price(self) -> float:
        """
        This method compute price for an amount.

        Returns
        -------
        float : price for this amount.
        """
        total = float()

        if self.weight == 200:

            total += int(self.amount) * \
                float(self.coffee.two_hundred_gram_price)

        elif self.weight == 1000:

            total += int(self.amount) * float(self.coffee.kilogram_price)

        return round(total, 4)
