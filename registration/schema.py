import graphene
from graphene import relay
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from graphene_django import DjangoObjectType

from registration.models import Information
from registration.decorators import login_required


class ContentTypeType(DjangoObjectType):
    class Meta:
        model = ContentType
        fields = ('id', 'app_label', 'model')


class PermissionType(DjangoObjectType):
    class Meta:
        model = Permission
        fields = ('id', 'name', 'content_type', 'codename')


class GroupType(DjangoObjectType):
    class Meta:
        model = Group
        fields = ('id', 'name', 'permissions')


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'user_permissions', 'groups', 'is_superuser')


class InformationUserType(DjangoObjectType):

    class Meta:
        model = Information
        fields = ('id', 'phone_number', 'user')


class Query(graphene.ObjectType):
    all_informations_users = graphene.List(
        InformationUserType)

    @login_required
    def resolve_all_informations_users(self, info):
        return Information.objects.select_related('user').all()
