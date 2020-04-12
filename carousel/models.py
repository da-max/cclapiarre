from django.db import models
from django.db.models.fields import CharField, IntegerField
from django.db.models.fields.files import ImageField

from ckeditor.fields import RichTextField



class Carousel(models.Model):
    ''' Model for carousel.
    
    
    title -- String for display title of carousel.
    image -- Background image of carousel.
    description -- Text for explain carousel.
    position -- Int for indicate position of carousel compared of other carousel.
    
    
    '''
    
    title = CharField(verbose_name="Titre du carousel", max_length=150)
    image = ImageField(verbose_name="Image que vous voulez afficher", upload_to="news/")
    description = RichTextField(verbose_name="Description du Carousel")
    position = IntegerField(verbose_name="Place du carousel par rapport au autre", help_text="Les carousels seront positionnés par rapport à ce nombre, si le nombre est\
        plus petit qu'un autre alors il se positionnera avant.", default=10)

    def __str__(self):
        ''' Display information for admin system.'''
        return "{} a une position {}".print(self.title, self.position)
