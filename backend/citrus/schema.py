from graphene import ObjectType
from graphene.relay import Node
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required, permission_required
from graphene_django_cud.mutations import DjangoBatchPatchMutation, DjangoUpdateMutation, DjangoDeleteMutation

from backend.citrus.models import CitrusAmount, CitrusOrder, CitrusProduct

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
    GraphQl type fro citrus.CitrusAmount model.
    """
    class Meta:
        model = CitrusAmount
        interfaces = (Node, )
        fields = '__all__'
        filter_fields = ['id']


class CitrusOrderType(DjangoObjectType):
    """
    GraphQL type for citrus.CitrusOrder model.
    """
    class Meta:
        model = CitrusOrder
        interfaces = (Node, )
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
        permission_required = ('citrus.change_citrusproduct', )


class UpdateCitrusProductMutation(DjangoUpdateMutation):
    """
    GraphQl mutation for Update CitrusProduct.
    """
    class Meta:
        model = CitrusProduct
        login_required = True
        permission_required = ('citrus.change_citrusproduct', )


class DeleteCitrusProductMutation(DjangoDeleteMutation):
    """
    GraphQl mutation for Delete CitrusProduct.
    """
    class Meta:
        model = CitrusProduct
        login_required = True
        permission_required = ('citrus.remove_citrusproduct', )


class Mutation(ObjectType):
    """ Define mutations for citrus app. """
    batch_patch_citrus_product = BatchPatchCitrusProductMutation.Field()
    update_citrus_product = UpdateCitrusProductMutation.Field()
    delete_citrus_product = DeleteCitrusProductMutation.Field()