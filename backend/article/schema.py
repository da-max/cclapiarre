from django.utils import timezone

import graphene
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphene_django.fields import Field

from backend.article.models import Article, Category
from backend.article.forms import ArticleForm


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ('id', 'name')


class ArticleType(DjangoObjectType):
    class Meta:
        model = Article
        fields = ('id', 'title', 'content',
                  'date_creation', 'category', 'author')


class AddArticle(DjangoModelFormMutation):
    """ Mutation for add article, this use form class,
    and modify perform_mutate method for get and save data
    in database.
    """
    article = Field(ArticleType)

    class Meta:
        form_class = ArticleForm

    def perform_mutate(form, info):
        """ This method save article in database and
        set many data (author, date_creation). """
        title = form.cleaned_data['title']
        content = form.cleaned_data['content']
        category = form.cleaned_data['category']

        article = Article.objects.create(
            title=title, content=content, category=category, date_creation=timezone.now(), author=info.context.user)

        return article

    def resolve_article(self, info, **kwargs):
        return self


class ChangeArticle(DjangoModelFormMutation):
    """ Mutation for change an article."""
    article = Field(ArticleType)

    class Meta:
        form_class = ArticleForm


class Query(graphene.ObjectType):
    all_articles = graphene.List(ArticleType)
    all_categories = graphene.List(CategoryType)

    def resolve_all_categories(self, info):
        return Category.objects.all()

    def resolve_all_articles(self, info):
        return Article.objects.select_related('category').all()


class Mutation(graphene.ObjectType):
    add_article = AddArticle.Field()
    change_article = ChangeArticle.Field()
