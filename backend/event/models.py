from django.db import models
from django.db.models.fields import DateField

from ckeditor.fields import RichTextField

class Event(models.Model):
    date = models.DateTimeField(verbose_name="Date et heure de l'évènement", help_text="Merci de rentrer la date et l'heure sous le format suivant : jj/mm/aaaa HH:mm")
    title = models.CharField(verbose_name="Titre de l'évènement", max_length=100)
    description = RichTextField(verbose_name="Description de l'évènement")

    def __str__(self):
        return "Le {} il se produiras : {}".format(self.date, self.title)

    class Meta:
        verbose_name = "Évènement"
