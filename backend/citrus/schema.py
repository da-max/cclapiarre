from graphene import ObjectType, Field
from graphene.relay import Node
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required, permission_required
from graphene_django_cud.mutations import DjangoBatchPatchMutation, DjangoUpdateMutation, DjangoDeleteMutation, \
    DjangoCreateMutation
from graphql_relay import from_global_id

from backend.citrus.models import CitrusAmount, CitrusOrder, CitrusProduct
from backend.registration.schema import UserLargeType


# Types
# =====


class CitrusProductType(DjangoObjectType):
    """ GraphQl type for citrus.CitrusProduct model. """

    class Meta:
        model = CitrusProduct
        interfaces = (Node,)
        fields = '__all__'
        filter_fields = ['id', 'name', 'display']


class CitrusAmountType(DjangoObjectType):
    """
    GraphQl type for citrus.CitrusAmount model.
    """

    class Meta:
        model = CitrusAmount
        interfaces = (Node,)
        fields = '__all__'
        filter_fields = ['id']


class CitrusOrderType(DjangoObjectType):
    """
    GraphQL type for citrus.CitrusOrder model.
    """
    user = Field(UserLargeType)

    class Meta:
        model = CitrusOrder
        interfaces = (Node,)
        fields = '__all__'
        filter_fields = ['id']


# Queries
# =======


class Query(ObjectType):
    """ Queries for citrus app. """
    citrus = DjangoFilterConnectionField(CitrusProductType)
    citrus_order = DjangoFilterConnectionField(CitrusOrderType)

    @login_required
    @permission_required('citrus.view_citrusproduct')
    def resolve_citrus(self, info, *args, **kwargs):
        return CitrusProduct.objects.all()

    @login_required
    @permission_required('citrus.view_citrusorder')
    def resolve_citrus_order(self, info, *args, **kwargs):
        return CitrusOrder.objects.all()


# Mutations
# ==========

class BatchPatchCitrusProductMutation(DjangoBatchPatchMutation):
    """
    GraphQl mutation for Patch CitrusProducts.
    """

    class Meta:
        model = CitrusProduct
        login_required = True
        permission_required = ('citrus.change_citrusproduct',)


class UpdateCitrusProductMutation(DjangoUpdateMutation):
    """
    GraphQl mutation for Update CitrusProduct.
    """

    class Meta:
        model = CitrusProduct
        login_required = True
        permission_required = ('citrus.change_citrusproduct',)


class DeleteCitrusProductMutation(DjangoDeleteMutation):
    """
    GraphQl mutation for Delete CitrusProduct.
    """

    class Meta:
        model = CitrusProduct
        login_required = True
        permission_required = ('citrus.remove_citrusproduct',)


class CreateCitrusAmountMutation(DjangoCreateMutation):
    """
    GraphQl mutation for create CitrusAmount
    """

    class Meta:
        model = CitrusAmount
        login_required = True
        permission_required = ('citrus.add_citrusamount',)
        exclude_fields = ('order',)


class CreateCitrusOrderMutation(DjangoCreateMutation):
    """
    GraphQl mutation for create CitrusOrder

    Methods
    -------
    mutate() -> dict:
        Methods for customise mutate of CitrusOrder
    """

    class Meta:
        model = CitrusOrder
        login_required = True
        permission_required = ('citrus.add_citrusorder',)
        exclude_fields = ('product', 'amounts', 'order')
        many_to_many_extras = {
            'amounts': {
                'add': {'type': 'CreateCitrusAmountInput'}
            }
        }

    @classmethod
    def mutate(cls, root, info: dict, **input: dict) -> dict:
        """

        Parameters
        ----------
        root
        info : dict
            Informations about the request.
        input : list
            Data send by frontend.

        Returns
        -------
        dict
            Dict with key 'citrus_order', value is the order create.
        """
        citrus = CitrusProduct.objects.filter(display=True)

        order = CitrusOrder.objects.get_or_create(user=info.context.user)
        amounts = input['input'].pop('amounts_add')

        for amount in amounts:
            product = citrus.get(id=from_global_id(amount['product'])[1])

            CitrusAmount.objects.update_or_create(product=product, order=order[0], defaults={
                'amount': amount['amount']
            })

        return {'citrus_order': order[0]}


class Mutation(ObjectType):
    """ Define mutations for citrus app. """
    add_citrus_order = CreateCitrusOrderMutation.Field()
    batch_patch_citrus_product = BatchPatchCitrusProductMutation.Field()
    delete_citrus_product = DeleteCitrusProductMutation.Field()
    update_citrus_product = UpdateCitrusProductMutation.Field()
