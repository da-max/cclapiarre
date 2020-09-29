import graphene
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphene_django.fields import Field

from carousel.models import Carousel
from carousel.forms import CarouselForm


class CarouselType(DjangoObjectType):
    class Meta:
        model = Carousel
        fields = '__all__'



class Query(graphene.ObjectType):
    all_carousels = graphene.List(CarouselType)

    def resolve_all_carousels(self, info):
        return Carousel.objects.all()
