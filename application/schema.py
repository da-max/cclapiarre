import graphene
from graphene.relay import Node
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from application.models import Application, ApplicationImage, \
    Option, Order, Product, Weight, Amount


class ApplicationImageType(DjangoObjectType):
    class Meta:
        model = ApplicationImage
        fields = '__all__'


class ApplicationType(DjangoObjectType):
    class Meta:
        model = Application
        fields = '__all__'
        interfaces = (Node, )


class OptionType(DjangoObjectType):
    class Meta:
        model = Option
        fields = '__all__'


class AmountType(DjangoObjectType):
    class Meta:
        model = Amount
        fields = '__all__'


class OrderType(DjangoObjectType):
    class Meta:
        interfaces = (Node, )
        model = Order
        fields = '__all__'
        filter_fields = ('id', 'application', 'user')


class ProductType(DjangoObjectType):
    class Meta:
        interfaces = (Node, )
        model = Product
        fields = '__all__'
        filter_fields = ['id', 'application']


class WeightType(DjangoObjectType):
    class Meta:
        model = Weight
        fields = '__all__'


class Query(graphene.ObjectType):
    all_applications = graphene.List(ApplicationType)
    product = Node.Field(ProductType)
    all_products = DjangoFilterConnectionField(ProductType)

    def resolve_all_products(self, info, *args, **kwargs):
        return Product.objects.all()

    def resolve_all_applications(self, info):
        return Application.objects.all()
