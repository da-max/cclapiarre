from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth import authenticate, login, logout

import graphene
from graphene import relay
from graphene_django import DjangoObjectType

import graphql_jwt
from graphql_jwt.decorators import login_required, token_auth
from graphql_jwt.shortcuts import get_token

from backend.registration.models import Information


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


class UserLargeType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'user_permissions', 'groups', 'is_superuser', 'information')


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', )


class InformationUserType(DjangoObjectType):

    class Meta:
        model = Information
        fields = ('id', 'phone_number', 'user')


class Login(graphene.Mutation):
    user = graphene.Field(UserLargeType)

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

        return cls(user=user)


class Logout(graphene.Mutation):
    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info):
        ok = True
        if not info.context.user.is_anonymous:
            try:
                logout(info.context)
            except Exception:
                ok = False
        return cls(ok=ok)


class Query(graphene.ObjectType):
    users = graphene.List(
        UserLargeType)
    user = graphene.Field(UserLargeType)

    @login_required
    def resolve_user(self, info, **kwargs):
        return info.context.user

    @login_required
    def resolve_users(self, info):
        return User.objects.all()


class Mutation(graphene.ObjectType):
    login = Login.Field()
    logout = Logout.Field()
