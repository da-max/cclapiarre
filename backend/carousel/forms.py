from django.forms import models, TextInput, Textarea, NumberInput

from backend.carousel.models import Carousel


class CarouselForm(models.ModelForm):
    ''' Form class based to model for create a form and upgrade/create
    the carousel.


    '''

    class Meta:
        ''' Meta class of CarouselForm

        model -- This class use Carousel model's for create the form.
        fields -- This form take all attributs of model.
        widget -- Define class for html element (uikit css framework).


        '''

        model = Carousel
        fields = '__all__'
        widgets = {
            'title': TextInput(attrs={'class': 'uk-input'}),
            'description': Textarea(attrs={'class': 'uk-textarea'}),
            'position': NumberInput(attrs={'class': 'uk-input'})
        }
