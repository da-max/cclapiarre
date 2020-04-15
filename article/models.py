""" Models for article app. """
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from humanize import naturalday

class Article(models.Model):
    """" Article model.
    title --- Title for article.
    contents --- Content of article.
    date_creation --- Creation_date_ of article.
    categorie --- Categorie of article, if cateogrie is private,
	this is hide for people if is not connect.
    author --- Author of article, define automatically with request.user
    """
    title = models.CharField(verbose_name="Titre de l'article",
                             max_length=60, help_text="60 caractéres maximum.")
    contents = RichTextField(verbose_name="Contenu de l'article",
                             config_name='awesome_ckeditor')
    date_creation = models.DateTimeField(verbose_name="Date de création de l'article",
                                         default=timezone.now, help_text="Laisser vide pour "
                                         "la date actuel")
    categorie = models.ForeignKey("Categorie", on_delete=models.CASCADE,
                                  help_text="La catégorie privée ne sera accéssible qu'aux "
                                  "personnes ayant un compte.")
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "{0} crée par {1} : {2}".format(self.title, self.author.username,
                                               naturalday(self.date_creation))

    class Meta:
        verbose_name = "Article"


class Categorie(models.Model):
    """ Categorie models for article app. """
    name = models.CharField(max_length=100, verbose_name="Nom de la catégorie")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Catégorie"
