from django.db.models import Model, CharField, URLField, BooleanField, DateTimeField
from django.utils import timezone

from ckeditor.fields import RichTextField
# Create your models here.


class PageAccess (Model):
    """ PageAccess class for list page with


    """

    name = CharField(max_length=255, verbose_name="Nom de la page d'accès")
    url = URLField(verbose_name="Lien de la page",
                   help_text="Rentrer ici le lien de la page pour lequel il faut gérer l'accès.", unique=True)
    access = BooleanField(default=True, verbose_name="Autoriser l'accès",
                          help_text="Cocher cette case afin d'autoriser l'accès à la page.")
    raise_exception = BooleanField(default=False, verbose_name='Lever une exception',
                                   help_text="Cette case n’a d’importance que si l’accès à la page est bloqué. Dans ce cas là, cocher cette case empêchera réellement l’accès à la page, en la déclarant introuvable.")
    title = CharField(verbose_name="Titre de la fenêtre",
                      help_text="Titre affiché sur la fenêtre empéchant l’accès à la page.", default="Vous êtes en avance (ou en retard) !", max_length=255)
    content = RichTextField(verbose_name="Message affiché", help_text="Message affiché sur la fenêtre empêchant l’accès à la page.",
                        default="Cette partie du site n'est pas encore ouverte, ou est fermée temporairement. Merci de repasser plus tard ou de contacter un gérant du site si vous rencontrez un problème.", max_length=500)
    start_date = DateTimeField(verbose_name="Date de prise en compte", default=timezone.now,
                        help_text="Si l’accès est bloqué, cette date sera prise en compte comme déclencheur du début du blocage de la page.")

    def __str__(self):

        return "L'url {} a un accès : {}".format(self.url, self.access)
