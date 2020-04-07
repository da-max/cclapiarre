from django.db.models import Model, CharField, URLField, BooleanField

# Create your models here.
class PageAccess (Model):
    """ PageAccess class for list page with
    
    
    """
    
    name = CharField(max_length=255, verbose_name="Nom de la page d'accès")
    url = URLField(verbose_name="Lien de la page", help_text="Rentrer ici le lien de la page pour lequel il faut gérer l'accès.")
    access = BooleanField(default=True, verbose_name="Autoriser l'accès", help_text="Cocher cette case afin d'autoriser l'accès à la page.")
    
    def __str__(self):
        
        return "L'url {} a un accès : {}".format(self.url, self.access)