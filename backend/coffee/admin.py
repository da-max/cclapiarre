from django.contrib import admin

from backend.coffee.models import Coffee, Type, Origin, CoffeeOrder, CoffeeAmount

admin.site.register(Coffee)
admin.site.register(Type)
admin.site.register(Origin)
admin.site.register(CoffeeOrder)
admin.site.register(CoffeeAmount)
