from django.utils import timezone

import graphene
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoFormMutation
from graphene_django.fields import Field

from article.models import Article, Category
from article.forms import ArticleForm


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ('id', 'name')


class ArticleType(DjangoObjectType):
    class Meta:
        model = Article
        fields = ('id', 'title', 'content',
                  'date_creation', 'category', 'author')


class ArticleMutation(DjangoFormMutation):
    article = Field(ArticleType)

    class Meta:
        form_class = ArticleForm

    def perform_mutate(form, info):
        title, content, category = form.cleaned_data[
            'title'], form.cleaned_data['content'], form.cleaned_data['category']
        article = Article.objects.create(
            title=title, content=content, category=category, date_creation=timezone.now(), author=info.context.user)
        return article


class Query(graphene.ObjectType):
    all_articles = graphene.List(ArticleType)

    def resolve_all_articles(self, info):
        return Article.objects.select_related('category').all()


class Mutation(graphene.ObjectType):
    create_article = ArticleMutation.Field()
