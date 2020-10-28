from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth import authenticate, login

import graphene
from graphene import relay
from graphene_django import DjangoObjectType

import graphql_jwt
from graphql_jwt.decorators import login_required, token_auth
from graphql_jwt.shortcuts import get_token

from backend.registration.models import Information
from backend.registration.decorators import login_required as personnal_login_required


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


class Login(graphene.Mutation):
    token = graphene.String()
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String()
        password = graphene.String()

    @classmethod
    def mutate(cls, root, info, username, password):
        user = authenticate(username=username, password=password)
        if user is None:
            raise Exception('Username or password are unavailable.')

        if not user.is_active:
            raise Exception('User are inactive.')

        login(info.context, user)

        return cls(token=get_token(user), user=user)


class Query(graphene.ObjectType):
    all_informations_users = graphene.List(
        InformationUserType)
    user = graphene.Field(UserType)

    @login_required
    def resolve_user(self, info, **kwargs):
        return info.context.user

    @personnal_login_required
    def resolve_all_informations_users(self, info):
        return Information.objects.select_related('user').all()


class Mutation(graphene.ObjectType):
    login = Login.Field()
