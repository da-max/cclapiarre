from django.contrib import admin

from coffee.models import Coffee, Type, Origin, CommandCoffee, Quantity

admin.site.register(Coffee)
admin.site.register(Type)
admin.site.register(Origin)
admin.site.register(CommandCoffee)
admin.site.register(Quantity)