from django.conf.urls import url
from django.urls import path

from django.contrib.auth.decorators import login_required

from article.views import home, CreateArticle, delete_article, UpdateArticle, ListArticle

urlpatterns = [
	url("liste-des-articles", ListArticle.as_view(), name="list_article"),
	url("creer-un-article", CreateArticle.as_view(), name="create_article"),
	path("supprimer-un-article/<int:id>", delete_article, name="delete_article"),
	path("modifier-un-article/<int:id_article>", UpdateArticle.as_view(), name="update_article"),
	url("accueil-privee", login_required(home), {"filtered":"Privé"}, name="list_article_private")
]

