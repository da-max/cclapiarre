from django.db.models import Model, ForeignKey, CASCADE
from django.db.models.fields import CharField
from django.db.models.fields import CharField, BooleanField, URLField

from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

class Informations(Model) :

    user = ForeignKey(User, verbose_name="Utilisateur", on_delete=CASCADE)
    phone_number = PhoneNumberField(verbose_name="Numéro de téléphone")

    def __str__(self):
        return "L'utilisateur {} a {} comme numéro de téléphone.".format(self.user.username, self.phone_number)



class PageAccess (Model):
    """ PageAccess class for list page with
    
    
    """
    
    name = CharField(max_length=255, verbose_name="Nom de la page d'accès")
    url = URLField(verbose_name="Lien de la page", help_text="Rentrer ici le lien de la page pour lequel il faut gérer l'accès.")
    access = BooleanField(default=True, verbose_name="Autoriser l'accès", help_text="Cocher cette case afin d'autoriser l'accès à la page.")
    
    def __str__(self):
        
        return "L'url {} a un accès : {}".format(self.url, self.access)