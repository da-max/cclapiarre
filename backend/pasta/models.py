from django.db.models import Model
from django.db.models import Model, ForeignKey, ManyToManyField, CASCADE
from django.db.models.fields import CharField, IntegerField, FloatField, BooleanField, TextField

from ckeditor.fields import RichTextField

from backend.coffee.models import Command

class Category(Model):
    """Category class for listing all category of product.
    Its take only on field : name with 100 caracteres max.

    name -- Fields for mark name of category of product


    """
    name = CharField(verbose_name='Nom de la categorie',
                     max_length=100, help_text="Maximum 100 caractéres.")
    description = TextField(verbose_name='Description de la catégorie', blank=True)

    class Meta:
        verbose_name = "Categorie"

    def __str__(self):
        return self.name

class Unit(Model):
    """Unit class for listing all unit of weigth of product.
    Its take only on field : name with 100 caracteres max.

    name -- Fields for mark name of unit.


    """
    name = CharField(verbose_name='Nom de l\'unité',
                     max_length=100, help_text="Maximum 100 caractéres.")

    class Meta:
        verbose_name = "Unité"
    
    def __str__(self):
        return self.name


class Product(Model):
    """Product class.

    name -- Fields for mark name of product of this producer.
    organic_agriculture --- BooleanField for mark if this product comes from organic farming.
    description --- RichTextField for mark one beautiful description of product, this field is optional
    maximum --- IntegerField to mark the maximum order quantity for this product.
    category --- ForeignKey towards Category table to save in what category this product belongs.


    """
    name = CharField(verbose_name="Nom du produit",
                     max_length=100, help_text="Maximum 100 caractéres.")
    organic_agriculture = BooleanField(verbose_name="Issue d'agriculture biologique", help_text="Cocher cette \
        case si le produit est issue de l'agriculture biologique.", default=False)
    description = RichTextField(verbose_name="Description du produit",
                                blank=True, help_text="Cette partie est facultative.")
    maximum = IntegerField(
        verbose_name="Quantité maximal commandable par utilisateur", default=100)

    class Meta:
        verbose_name = "Produit"
    
    def __str__(self):
        return self.name



class MetadataProduct(Model):
    """MetadataProduct class for save price, weigth of one product.

    A product can have several weights (and therefore several prices)
    this model is therefore used to complete a product.

    product --- ForeignKey towards Product table.
    weight --- Weight of product.
    unit --- In what unit is weight.
    price --- Pirce of product for this weight.



    """
    product = ForeignKey(Product, on_delete=CASCADE)
    weight = FloatField(verbose_name="Poids du produit")
    unit = ForeignKey(Unit, on_delete=CASCADE)
    price = FloatField(verbose_name="Prix du produit")
    display = BooleanField(verbose_name="Afficher le produit", help_text="Cocher cette case\
        afin que le produit soit affiché sur le tableau.", default=True)
    category = ForeignKey(Category, on_delete=CASCADE)
    
    def __str__(self):
        return "Le produit {} a un poids de {} {} pour \
            un prix de {} €".format(self.product.name, self.weight, self.unit.name, self.price)

    class Meta:
        verbose_name = "Metadata"
    
    
class CommandPasta(Command):
    """This class extends to Command Model, this define all basics
    fields.
    
    command --- ManyToManyField to Amount models.
    
    
    
    """
    product = ManyToManyField(MetadataProduct, through='Amount')
    
    def __str__(self):
        return "Commande faites par {} {}".format(self.name, self.first_name)
    
    class Meta:
        verbose_name = "Commande de pâte"
    
    def get_total_price(self):
        """ Function than return price for a command. """
        amounts = Amount.objects.filter(command=self)
        
        total_price = float()
        
        for amount in amounts:
            total_price += float(amount.product.price * amount.amount)
        
        return round(total_price, 3)
        


class Amount(Model):
    
    command = ForeignKey(CommandPasta, on_delete=CASCADE)
    product = ForeignKey(MetadataProduct, on_delete=CASCADE)
    amount = FloatField(verbose_name="Quantité commandé")
    
    
    def __str__(self):
        return "{} a commandé {} de {}".format(self.command.name, self.amount, self.product.product.name)
    
    
    def get_price(self):
        """ Function than return price for product """    
        price = float(self.product.price) * float(self.amount)
        return round(price, 3)