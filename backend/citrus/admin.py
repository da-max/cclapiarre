from django.contrib import admin
from django.contrib.admin import ModelAdmin

from backend.citrus.models import CitrusProduct, CitrusOrder, CitrusAmount

class CitrusProductAdmin(ModelAdmin):

    def display(self, request, queryset):
        queryset.update(display=True)

    def hide(self, request, queryset):
        queryset.update(display=False)

    def get_actions(self, request):

        actions = super().get_actions(request)
        if request.user.is_superuser == False:
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

    hide.short_description = "Cacher les produits séléctionnés"
    display.short_description = "Afficher les produits séléctionnés"
    actions = [display, hide]

    list_display = ('name', 'display', 'price')
    list_filter = ('weight', 'display')
    ordering = ('display', )
    search_fields = ['name']

class CitrusOrderAdmin(ModelAdmin):

    list_display = ("user", "number")
    list_filter = ["user"]
    ordering = ('user',)
    search_fields = ['user']

class CitrusAmountAdmin(ModelAdmin):

    list_display = ("order", "product", "amount")
    list_filter = ["order", "product"]
    ordering = ('order', )
    search_fields = ['order', "product"]

admin.site.register(CitrusOrder, CitrusOrderAdmin)
admin.site.register(CitrusProduct, CitrusProductAdmin)
admin.site.register(CitrusAmount, CitrusAmountAdmin)
