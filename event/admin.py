from django.contrib import admin
from event.models import Event
from django.contrib.admin import ModelAdmin

class EventAdmin(ModelAdmin):

    list_display = ('title', 'date')
    search_fields = ('titre', 'date', 'description')
    ordering = ['date']

admin.site.register(Event, EventAdmin)
#admin.site.register(Categorie)
#admin.site.register(Delivery)
#admin.site.register(DateLimitUser)
#admin.site.register(DateLimitCC)
