from django.utils.text import Truncator

from django.contrib import admin
from django.contrib.admin import ModelAdmin

from backend.article.models import Article, Category


class ArticleAdmin(ModelAdmin):

    def save_model(self, request, obj, form, change):

        obj.author = request.user
        super().save_model(request, obj, form, change)

    fieldsets = [
        ("Contenu", {'fields': ['title', 'content']}),
        ("Catégorie (obligatoire)", {'fields': ['category']})
    ]

    exclude = ['date_creation', 'author']
    list_display = ('title', 'author', "date_creation")
    list_filter = ('category',)
    date_hierarchy = 'date_creation'
    ordering = ("date_creation", )
    search_fields = ['title', "content"]


class CategorieAdmin(ModelAdmin):

    list_display = ('name', )
    list_filter = ('name', )
    ordering = ("name", )
    search_fields = ['name']


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategorieAdmin)
