import graphene
from graphene.relay import Node
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.forms.mutation import DjangoModelFormMutation

from backend.application.models import Application, ApplicationImage, \
    Option, Order, Product, Weight, Amount
from backend.application.forms import ProductForm
from backend.registration.decorators import login_required, permissions_required, application_permissions_required


# Types
# =========

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
        filter_fields = ['id', 'application__name']


class AmountType(DjangoObjectType):
    class Meta:
        model = Amount
        fields = '__all__'


class OrderType(DjangoObjectType):
    class Meta:
        interfaces = (Node, )
        model = Order
        fields = '__all__'
        filter_fields = ['id', 'application__name', 'user']


class ProductType(DjangoObjectType):
    class Meta:
        interfaces = (Node, )
        model = Product
        fields = '__all__'
        filter_fields = [
            'id', 'application__slug', 'application__name', 'display']


class WeightType(DjangoObjectType):
    class Meta:
        interfaces = (Node, )
        model = Weight
        fields = '__all__'
        filter_fields = ['id', 'application__name']


# Nodes
# =========

class ApplicationNode(DjangoObjectType):
    class Meta:
        model = Application
        filter_fields = ['slug', 'name', 'id']
        interfaces = (Node, )


# Mutations
# ==========

class AddProduct(DjangoModelFormMutation):

    product = graphene.Field(ProductType)

    class Meta:
        form_class = ProductForm

    @classmethod
    def perform_mutate(form, info):
        print(form)
        return True

    def resolve_product(self, info, **kwargs):
        return self

    # @staticmethod
    # def mutate(self, info, *args, **kwargs):
    #     print(self)
    #     return True


class Mutation(graphene.ObjectType):
    add_product = AddProduct.Field()


# Queries
# =========

class Query(graphene.ObjectType):
    all_applications = graphene.List(ApplicationType)
    product = Node.Field(ProductType)
    application_products = DjangoFilterConnectionField(ProductType)
    all_options = DjangoFilterConnectionField(OptionType)
    all_weight = DjangoFilterConnectionField(WeightType)
    application_order = DjangoFilterConnectionField(OrderType)
    application_by_slug = graphene.Field(
        ApplicationType, slug=graphene.String())

    @login_required
    def resolve_application_by_slug(self, info, slug, *args, **kwargs):
        return Application.objects.get(slug=slug)

    @login_required
    @application_permissions_required('members')
    def resolve_all_options(self, info, application__slug, *args, **kwargs):
        return Option.objects.all()

    @login_required
    @application_permissions_required('members')
    def resolve_application_products(self, info, *args, **kwargs):
        return Product.objects.all()

    def resolve_all_applications(self, info):
        return Application.objects.all()

    @login_required
    @application_permissions_required('members')
    def resolve_all_weight(self, info, application__slug, *args, **kwargs):
        return Weight.objects.all()

    @login_required
    @application_permissions_required('admins')
    def resolve_application_order(self, info, application__slug, *args, **kwargs):
        return Order.objects.all()
