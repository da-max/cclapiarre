import graphene
from graphene.relay import Node
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django_cud.mutations import DjangoCreateMutation
from graphql_jwt.decorators import login_required, permission_required

from backend.coffee.models import Amount, Coffee, Order, Origin, Type
from graphene_django import DjangoObjectType

# Types
# ========


class CoffeeOriginType(DjangoObjectType):
    """ GraphQL type for coffee.Origin model. """
    class Meta:
        model = Origin
        interfaces = (Node, )
        fields = '__all__'
        filter_fields = ['id', 'coffee']


class CoffeeTypeType(DjangoObjectType):
    """ GraphQL type for coffee.Type model. """
    class Meta:
        model = Type
        interfaces = (Node, )
        fields = '__all__'
        filter_fields = ['id', 'coffee']


class CoffeeType(DjangoObjectType):
    """ GrapQL type for coffee.Coffee model. """
    class Meta:
        model = Coffee
        interfaces = (Node, )
        fields = '__all__'
        filter_fields = ['id', 'display']


class CoffeeOrderType(DjangoObjectType):
    """ GraphQL type for coffee.Order model. """
    class Meta:
        model = Order
        interfaces = (Node, )
        fields = '__all__'
        filter_fields = ['id']


class CoffeeAmountType(DjangoObjectType):
    """ GraphQL type for coffee.Amount model. """
    class Meta:
        model = Amount
        interfaces = (Node, )
        fields = '__all__'
        filter_fields = ['coffee__farm_coop']

# Queries
# =======


class Query(graphene.ObjectType):
    """ Define queries for coffee app. """
    coffee_type = DjangoFilterConnectionField(CoffeeTypeType)
    coffee_origin = DjangoFilterConnectionField(CoffeeOriginType)
    coffee = DjangoFilterConnectionField(CoffeeType)
    coffee_order = DjangoFilterConnectionField(CoffeeOrderType)
    coffee_amount = DjangoFilterConnectionField(CoffeeAmountType)

    @login_required
    @permission_required('coffee.view_type')
    def resolve_coffee_type(self, info, *args, **kwargs) -> Type:
        return Type.objects.all()

    @login_required
    @permission_required('coffee.view_origin')
    def resolve_coffee_origin(self, info, *args, **kwargs) -> Origin:
        return Origin.objects.all()

    @login_required
    @permission_required('coffee.view_coffee')
    def resolve_coffee(self, info, *args, **kwargs) -> Coffee:
        return Coffee.objects.all()

    @login_required
    @permission_required('coffee.view_order')
    def resolve_coffee_order(self, info, *args, **kwargs) -> Order:
        return Order.objects.all()

    @login_required
    @permission_required('coffee.view_amount')
    def resolve_coffee_amount(self, info, *args, **kwargs) -> Order:
        return Amount.objects.all()

# Mutations
# =========


class CreateOriginMutation(DjangoCreateMutation):
    """ GraphQL mutation for create Origin. """
    class Meta:
        model = Origin
        login_required = True
        permission_required = ('coffee.add_origin',)


class CreateTypeMutation(DjangoCreateMutation):
    """ GraphQL mutation for create Type. """
    class Meta:
        model = Type
        login_required = True
        permission_required = ('coffee.add_type', )


class CreateCoffeeMutation(DjangoCreateMutation):
    """ GraphQL mutation for create Coffee. """
    class Meta:
        model = Coffee
        login_required = True
        permission_required = ('coffee.add_coffee', )


class Mutation(graphene.ObjectType):
    """ Define mutations for coffee app. """
    add_coffee_origin = CreateOriginMutation.Field()
    add_coffee_type = CreateTypeMutation.Field()
    add_coffee = CreateCoffeeMutation.Field()
