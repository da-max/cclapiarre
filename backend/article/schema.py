from django.utils import timezone

import graphene
from graphene_django import DjangoObjectType
from graphene_django.fields import Field
from graphene_django_cud.mutations import DjangoCreateMutation, DjangoUpdateMutation

from backend.article.forms import ArticleForm
from backend.article.models import Article, Category
from backend.registration.schema import UserLargeType


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ('id', 'name')


class ArticleType(DjangoObjectType):
    author = graphene.Field(UserLargeType)

    class Meta:
        model = Article
        fields = ('id', 'title', 'content',
                  'date_creation', 'category', 'author')


class CreateArticleMutations(DjangoCreateMutation):
    """
    Class for define CreateArticle mutation.
    """
    class Meta:
        model = Article
        permission_required = ('article.add_article',)
        login_required = True
        exclude_fields = ('date_creation', 'author')
        auto_context_fields = {
            'author': 'user'
        }


class UpdateArticleMutation(DjangoUpdateMutation):
    """ Mutation for change an article."""

    class Meta:
        model = Article
        permission_required = ('article.change_article',)
        login_required = True


class Query(graphene.ObjectType):
    all_articles = graphene.List(ArticleType)
    all_categories = graphene.List(CategoryType)

    def resolve_all_categories(self, info):
        return Category.objects.all()

    def resolve_all_articles(self, info):
        return Article.objects.select_related('category').all()


class Mutation(graphene.ObjectType):
    add_article = CreateArticleMutations.Field()
    change_article = UpdateArticleMutation.Field()
