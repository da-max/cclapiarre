from django.forms import models, TextInput, Textarea, ChoiceField
from django.forms.widgets import Select

from article.models import Article, Categorie


class ArticleForm(models.ModelForm):
	""" Class for create or update an article.
	It extends ModelForm class. And define a Meta class
	for add model name and other informations for display.

	"""
	class Meta:
		model = Article
		exclude = ["date_creation", "author"]
		widgets = {
			"title" : TextInput(attrs={"class" : "uk-input"}),
			"contents" : Textarea(attrs={"class": "uk-textarea"}),
			"categorie" : Select({"class":"uk-select"})
		}