from django.db.models import Model, OneToOneField, CASCADE

from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Information(Model):

    user = OneToOneField(
        User, verbose_name="Utilisateur", on_delete=CASCADE, related_name='information')
    phone_number = PhoneNumberField(verbose_name="Numéro de téléphone")

    def __str__(self):
        return "L'utilisateur {} a {} comme numéro de téléphone.".format(self.user.username, self.phone_number)
