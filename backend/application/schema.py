from django.contrib.auth.models import User

import graphene
from graphene.relay import Node
from graphql_relay import from_global_id, to_global_id
from graphene_django import DjangoObjectType, DjangoListField
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphql_jwt.decorators import login_required
from graphene_django_cud.mutations import DjangoCreateMutation, DjangoUpdateMutation


from backend.application.models import Application, ApplicationImage, \
    Option, Order, Product, Weight, Amount
from backend.application.views import order_added
from backend.application.forms import ApplicationForm, ProductForm
from backend.registration.schema import UserType, UserLargeType
from backend.registration.decorators import check_application_permission_by_slug


# Types
# =========

class ApplicationImageType(DjangoObjectType):
    """GraphQl type for ApplicationImage model."""
    class Meta:
        model = ApplicationImage
        fields = '__all__'


class ApplicationType(DjangoObjectType):
    """
    GraphQl type for Application model.

    Methods
    -------
    resolve_members() -> User:
        Method for customise resolve of members fields and check if user is authenticated.
    resolve_admins() -> User:
        Method for customise resolve of admins and check if user is authenticated.
    """
    members = graphene.List(graphene.ID)
    admins = graphene.List(graphene.ID)

    class Meta:
        model = Application
        fields = '__all__'
        interfaces = (Node, )

    def resolve_members(self, info) -> list:
        """ Method for customise resolve of members and check if user is authenticated. """
        return [
            to_global_id('UserLargeType', member.id)
            for member in User.objects.filter(member_application=self)
        ]

    def resolve_admins(self, info) -> graphene.ID:
        """ Method for customise resolve of admins and check if user is authenticated. """
        return [
            to_global_id('UserLargeType', admin.id)
            for admin in User.objects.filter(admin_application=self)
        ]


class OptionType(DjangoObjectType):
    """GraphQl type for Option model."""
    class Meta:
        model = Option
        fields = '__all__'
        interfaces = (Node, )
        filter_fields = ['id', 'application__name', 'application__slug']


class AmountType(DjangoObjectType):
    """GraphQl type for Amount model."""
    class Meta:
        model = Amount
        fields = '__all__'


class OrderType(DjangoObjectType):
    """
    GraphQl type for Order model.

    Attributes
    ----------
    user_full : graphene.Field

    Methods
    -------
    resolve_user_full() -> User:
        Method for resolve user_full field and get all info of User.
    """
    class Meta:
        interfaces = (Node, )
        model = Order
        fields = '__all__'
        filter_fields = ['id', 'application__name', 'application__slug']

    user_full = graphene.Field(UserLargeType)

    def resolve_user_full(self, info) -> User:
        return User.objects.filter(order=self).get(id=self.user.id)


class ProductType(DjangoObjectType):
    """GraphQl type for Product model."""
    class Meta:
        interfaces = (Node, )
        model = Product
        fields = '__all__'
        filter_fields = [
            'id', 'application__slug', 'application__name', 'display']


class WeightType(DjangoObjectType):
    """GraphQl type for Weight model."""
    class Meta:
        interfaces = (Node, )
        model = Weight
        fields = '__all__'
        filter_fields = ['id', 'application__name',  'application__slug']


# Mutations
# ==========

class CreateProductMutation(DjangoCreateMutation):
    """GraphQl mutation for create Product."""
    class Meta:
        model = Product
        login_required = True


class CreateAmountMutation(DjangoCreateMutation):
    """GraphQl mutation for create Amount."""
    class Meta:
        model = Amount
        login_required = True
        exclude_fields = ('order', )


class CreateOrderMutation(DjangoCreateMutation):
    """
    GraphQl mutation for create Order.

    Methods
    -------
    mutate() -> dict:
        Methods for customise mutate of Order.
    """
    class Meta:
        model = Order
        login_required = True
        exclude_fields = ('products', 'amount_set', 'user')
        many_to_many_extras = {
            "amount_set": {
                "add": {"type": "CreateAmountInput"}
            }
        }

    @classmethod
    def mutate(cls, root, info, **input) -> dict:
        """Methods for customise mutate of Order."""
        application = Application.objects.get(
            id=input['input']['application'])

        products = Product.objects.filter(display=True)
        options = Option.objects.filter(application=application.id)
        weights = Weight.objects.filter(application=application.id)

        order = Order.objects.get_or_create(
            user=info.context.user, application=application)

        amounts = input['input'].pop('amount_set_add')
        for amount in amounts:
            # from_global_id is use because input contains id generate by the Node interface.
            weight = weights.get(id=from_global_id(amount['weight'])[1])
            product = products.get(id=from_global_id(amount['product'])[1])

            if amount['option'] and product.options != Option.objects.none():
                option = options.get(id=from_global_id(amount['option'])[1])
                amount = Amount.objects.update_or_create(
                    product=product, option=option, weight=weight, order=order[0], defaults={'amount': amount['amount']})
            else:
                amount = Amount.objects.update_or_create(
                    product=product, weight=weight, order=order[0], defaults={'amount': amount['amount']})
        order_added.send(sender=cls.__class__, order=order[0], create=order[1])
        return {'order': order[0]}


class CreateOptionMutation(DjangoCreateMutation):
    """GraphQl mutation for create Option."""
    class Meta:
        model = Option
        login_required = True


class CreateWeightMutation(DjangoCreateMutation):
    """GraphQl mutation for create Weight."""
    class Meta:
        model = Weight
        login_required = True
        permissions = ('application.add_weight', )


class UpdateApplicationMutation(DjangoUpdateMutation):
    """GraphQl mutation for update Application."""

    class Meta:
        model = Application
        login_required = True
        exclude_fields = ('slug',)
        optional_fields = ('images', 'description', 'table', 'admins', 'members')


class UpdateProductMutation(DjangoUpdateMutation):
    """ GraphQl mutation for update Product. """
    class Meta:
        model = Product
        login_required = True


class Mutation(graphene.ObjectType):
    add_product = CreateProductMutation.Field()
    create_order = CreateOrderMutation.Field()
    add_option = CreateOptionMutation.Field()
    add_weight = CreateWeightMutation.Field()

    update_application = UpdateApplicationMutation.Field()
    update_product = UpdateProductMutation.Field()


# Queries
# =========

class Query(graphene.ObjectType):
    all_applications = DjangoListField(ApplicationType)
    product = Node.Field(ProductType)
    all_products = DjangoFilterConnectionField(ProductType)
    all_options = DjangoFilterConnectionField(OptionType)
    all_weight = DjangoFilterConnectionField(WeightType)
    application_order = DjangoFilterConnectionField(OrderType)
    application_by_slug = graphene.Field(
        ApplicationType, slug=graphene.String())

    @login_required
    def resolve_application_by_slug(self, info, slug, *args, **kwargs):
        return Application.objects.get(slug=slug)

    @login_required
    @check_application_permission_by_slug('member')
    def resolve_all_options(self, info, *args, **kwargs):
        return Option.objects.all()

    @login_required
    @check_application_permission_by_slug('member')
    def resolve_application_products(self, info, *args, **kwargs):
        return Product.objects.all()

    def resolve_all_applications(self, info, *args, **kwargs):
        return Application.objects.all()

    @login_required
    @check_application_permission_by_slug('member')
    def resolve_all_weight(self, info, *args, **kwargs):
        return Weight.objects.all()

    @login_required
    @check_application_permission_by_slug('admin')
    def resolve_application_order(self, info, *args, **kwargs):
        return Order.objects.all()
