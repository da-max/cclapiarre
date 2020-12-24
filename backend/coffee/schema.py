from django.db.models import Q
import graphene
from graphene.relay import Node
from graphql_relay import from_global_id
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django_cud.mutations import DjangoCreateMutation
from graphql_jwt.decorators import login_required, permission_required

from backend.registration.schema import UserLargeType
from backend.coffee.models import CoffeeAmount, Coffee, CoffeeOrder, Origin, Type
from backend.coffee.views import coffee_order_add

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
    user = graphene.Field(UserLargeType)

    class Meta:
        model = CoffeeOrder
        interfaces = (Node, )
        fields = '__all__'
        filter_fields = ['id', 'user__id']


class CoffeeAmountType(DjangoObjectType):
    """ GraphQL type for coffee.CoffeeAmount model. """
    class Meta:
        model = CoffeeAmount
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
    def resolve_coffee_order(self, info, *args, **kwargs) -> CoffeeOrder:
        return CoffeeOrder.objects.all()

    @login_required
    @permission_required('coffee.view_amount')
    def resolve_coffee_amount(self, info, *args, **kwargs) -> CoffeeOrder:
        return CoffeeAmount.objects.all()

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


class CreateCoffeeAmountMutation(DjangoCreateMutation):
    class Meta:
        model = CoffeeAmount
        login_required = True
        exclude_fields = ('order')


class CreateCoffeeOrderMutation(DjangoCreateMutation):
    """
    GraphQl mutation for create Order.

    Methods
    -------
    mutate() -> dict;
        Methods for customise mutate of Order.
    """
    class Meta:
        model = CoffeeOrder
        login_required = True
        permission_required = ('coffee.add_order', )
        exclude_fields = ('coffee', 'amounts', 'user')
        many_to_many_extras = {
            "amounts": {
                "add": {"type": "CreateCoffeeAmountInput"}
            }
        }

    @classmethod
    def mutate(cls, root, info, **input) -> dict:
        """ Methods for customise mutate of Order"""
        coffees = Coffee.objects.filter(display=True)
        types = Type.objects.all()

        order = CoffeeOrder.objects.get_or_create(user=info.context.user)
        amounts = input['input'].pop('amounts_add')

        for amount in amounts:
            coffee = coffees.get(id=from_global_id(amount['coffee'])[1])
            t = types.get(
                Q(id=from_global_id(amount['sort'])[1]), Q(coffee=coffee))

            amount = CoffeeAmount.objects.update_or_create(
                coffee=coffee, sort=t, order=order[0], weight=amount['weight'], defaults={
                    'amount': amount['amount']}
            )

        coffee_order_add.send(sender=cls.__class__,
                              order=order[0], create=order[1])
        return {'coffee_order': order[0]}


class Mutation(graphene.ObjectType):
    """ Define mutations for coffee app. """
    add_coffee_origin = CreateOriginMutation.Field()
    add_coffee_type = CreateTypeMutation.Field()
    add_coffee = CreateCoffeeMutation.Field()
    add_coffee_order = CreateCoffeeOrderMutation.Field()
