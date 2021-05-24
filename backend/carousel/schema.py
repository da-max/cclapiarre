import graphene
from graphene_django import DjangoObjectType
from graphene_django_cud.mutations import DjangoCreateMutation, DjangoUpdateMutation, DjangoDeleteMutation

from backend.carousel.models import Carousel


class CarouselType(DjangoObjectType):
    class Meta:
        model = Carousel
        fields = '__all__'


class CreateCarouselMutation(DjangoCreateMutation):
    """ GraphQl mutation for create Carousel. """

    class Meta:
        model = Carousel
        login_required = True,
        permissions = ('carousel.add_carousel', )


class DeleteCarouselMutation(DjangoDeleteMutation):
    """ Mutation for delete a carousel. """
    class Meta:
        model = Carousel
        login_required = True
        permissions = ('carousel.delete_carousel',)


class UpdateCarouselMutation(DjangoUpdateMutation):
    """ Mutation for update a carousel. """
    class Meta:
        model = Carousel
        login_required = True
        permissions = ('carousel.change_carousel',)


class Query(graphene.ObjectType):
    all_carousels = graphene.List(CarouselType)

    def resolve_all_carousels(self, info):
        return Carousel.objects.all().order_by('position')


class Mutation(graphene.ObjectType):
    """ Define mutations for carousel app. """
    add_carousel = CreateCarouselMutation.Field()
    delete_carousel = DeleteCarouselMutation.Field()
    update_carousel = UpdateCarouselMutation.Field()
