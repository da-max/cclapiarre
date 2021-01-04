from django.conf.urls import url
from django.urls import path

from backend.article.views import CreateArticle, delete_article, UpdateArticle, ListArticle

urlpatterns = [
    url("liste-des-articles", ListArticle.as_view(), name="list_article"),
    url("creer-un-article", CreateArticle.as_view(), name="create_article"),
    path("supprimer-un-article/<int:id_article>",
         delete_article, name="delete_article"),
    path("modifier-un-article/<int:id_article>",
         UpdateArticle.as_view(), name="update_article")
]
