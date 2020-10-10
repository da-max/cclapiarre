from django.db.models import Model, ForeignKey, CASCADE
from django.db.models.fields import CharField
from django.db.models.fields import CharField, BooleanField, URLField

from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

class Information(Model) :

    user = ForeignKey(User, verbose_name="Utilisateur", on_delete=CASCADE)
    phone_number = PhoneNumberField(verbose_name="Numéro de téléphone")

    def __str__(self):
        return "L'utilisateur {} a {} comme numéro de téléphone.".format(self.user.username, self.phone_number)