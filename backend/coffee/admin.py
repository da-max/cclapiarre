from django.contrib import admin

from backend.coffee.models import Coffee, Type, Origin, Order, Amount

admin.site.register(Coffee)
admin.site.register(Type)
admin.site.register(Origin)
admin.site.register(Order)
admin.site.register(Amount)
