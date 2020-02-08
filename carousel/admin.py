from django.contrib import admin
from django.contrib.admin import ModelAdmin

from carousel.models import Carousel

class CarouselAdmin(ModelAdmin):
    
    list_display = ['title', 'position']
    search_fields = ['title', 'description']
    ordering = ('position',)

admin.site.register(Carousel, CarouselAdmin)
