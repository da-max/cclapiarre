from django.contrib.auth.models import User

import graphene
from graphene.relay import Node
from graphql_relay import from_global_id
from graphene_django import DjangoObjectType, DjangoListField
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphql_jwt.decorators import login_required
from graphene_django_cud.mutations import DjangoCreateMutation


from backend.application.models import Application, ApplicationImage, \
    Option, Order, Product, Weight, Amount
from backend.application.forms import ApplicationForm, ProductForm
from backend.registration.schema import UserType
from backend.registration.decorators import check_application_permission_by_slug


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

    def resolve_members(self, info):
        members = User.objects.filter(member_application=self)
        if info.context.user.is_authenticated:
            return members
        else:
            return members.only('id')

    def resolve_admins(self, info):
        if info.context.user.is_authenticated:
            return User.objects.filter(admin_application=self)
        else:
            return User.objects.filter(admin_application=self).only('id')


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


# Mutations
# ==========

class AddProduct(DjangoModelFormMutation):

    product = graphene.Field(ProductType)

    class Meta:
        form_class = ProductForm

    def resolve_product(self, info, **kwargs):
        return self

    # @staticmethod
    # def mutate(self, info, *args, **kwargs):
    #     print(self)
    #     return True


class UpdateApplication(DjangoModelFormMutation):

    application = graphene.Field(ApplicationType)

    class Meta:
        form_class = ApplicationForm


class CreateAmountMutation(DjangoCreateMutation):
    class Meta:
        model = Amount
        login_required = True
        exclude_fields = ('order', )


class CreateOrderMutation(DjangoCreateMutation):
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
    def mutate(cls, root, info, **input):
        application = Application.objects.get(
            id=input['input']['application'])
        order = Order.objects.create(
            user=info.context.user, application=application)

        products = Product.objects.all()
        options = Option.objects.all()
        weights = Weight.objects.all()
        amounts = input['input'].pop('amount_set_add')
        for amount in amounts:
            weight = weights.get(id=from_global_id(amount['weight'])[1])
            product = products.get(id=from_global_id(amount['product'])[1])

            if amount['option']:
                option = options.get(id=from_global_id(amount['option'])[1])
                amount = Amount(
                    product=product, option=option, weight=weight, amount=amount['amount'], order=order).save()
            else:
                amount = Amount(
                    product=product, weight=weight, amount=amount['amount'], order=order).save()
        return {'order': order}


class Mutation(graphene.ObjectType):
    add_product = AddProduct.Field()
    create_order = CreateOrderMutation.Field()
    # add_amount_order = AddAmountOrder.Field()
    update_application = UpdateApplication.Field()


# Queries
# =========

class Query(graphene.ObjectType):
    all_applications = DjangoListField(ApplicationType)
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
    def resolve_all_options(self, info, *args, **kwargs):
        return Option.objects.all()

    @login_required
    @check_application_permission_by_slug('admin')
    def resolve_application_products(self, info, *args, **kwargs):
        return Product.objects.all()

    def resolve_all_applications(self, info, *args, **kwargs):
        return Application.objects.all()

    @login_required
    def resolve_all_weight(self, info, *args, **kwargs):
        return Weight.objects.all()

    @login_required
    def resolve_application_order(self, info, *args, **kwargs):
        return Order.objects.all()
