from django.db import models


class Application(models.Model):
    """ Application model, this model is use by many of the following models
    because it describes the core of the created application. 


    """
    name = models.CharField(verbose_name="Nom de l’application", max_lenght=60)
