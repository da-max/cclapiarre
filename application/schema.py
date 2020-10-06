import graphene
from graphene.relay import Node
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from application.models import Application, ApplicationImage, \
    Option, Order, Product, Weight, Amount
from registration.decorators import login_required, permissions_required, application_permissions_required


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
        interfaces = (Node, )
        filter_fields = ['id', 'application']


class AmountType(DjangoObjectType):
    class Meta:
        model = Amount
        fields = '__all__'


class OrderType(DjangoObjectType):
    class Meta:
        interfaces = (Node, )
        model = Order
        fields = '__all__'
        filter_fields = ['id', 'application', 'user']


class ProductType(DjangoObjectType):
    class Meta:
        interfaces = (Node, )
        model = Product
        fields = '__all__'
        filter_fields = ['id', 'application__name']


class WeightType(DjangoObjectType):
    class Meta:
        interfaces = (Node, )
        model = Weight
        fields = '__all__'
        filter_fields = ['id', 'application']


class Query(graphene.ObjectType):
    all_applications = graphene.List(ApplicationType)
    product = Node.Field(ProductType)
    application_products = DjangoFilterConnectionField(ProductType)
    all_options = DjangoFilterConnectionField(OptionType)
    all_weight = DjangoFilterConnectionField(WeightType)

    @login_required
    def resolve_all_options(self, info, *args, **kwargs):
        return Option.objects.all()

    @login_required
    @application_permissions_required('members')
    def resolve_application_products(self, info, application_name):
        try:
            return Product.objects.all()
        except Product.DoesNotExist:
            return None

    def resolve_all_applications(self, info):
        return Application.objects.all()

    @login_required
    def resolve_all_weight(self, info):
        return Weight.objects.all()
