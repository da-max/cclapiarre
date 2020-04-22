from django.contrib import admin
from django.contrib.admin import ModelAdmin

from citrus.models import Product, Command, Amount

class ProductAdmin(ModelAdmin):

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

class CommandAdmin(ModelAdmin):

    list_display = ("user", "number")
    list_filter = ["user"]
    ordering = ('user',)
    search_fields = ['user']

class AmountAdmin(ModelAdmin):

    list_display = ("command", "product", "amount")
    list_filter = ["command", "product"]
    ordering = ('command', )
    search_fields = ['command', "product"]

admin.site.register(Command, CommandAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Amount, AmountAdmin)
