from django.conf.urls import url
from django.urls import path

from backend.coffee.views import ListCoffee, ListOrigin, UpdateOrigin, CreateOrigin, delete_origin, pdf_list_command, global_command, pdf_global_command, \
    CreateCoffee, UpdateCoffee, delete_coffee

urlpatterns = [

    # Coffee
    url("liste-des-cafe", ListCoffee.as_view(), name='list_coffee'),
    url("creer-un-cafe", CreateCoffee.as_view(), name="create_coffee"),
    path('modifier-un-cafe/<int:id_coffee>',
         UpdateCoffee.as_view(), name='update_coffee'),
    path('supprimer-un-cafe/<int:id_coffee>',
         delete_coffee, name='delete_coffee'),

    # Origin
    url('liste-des-origines', ListOrigin.as_view(), name="list_origin"),
    path('modifier-une-origine/<int:id_origin>',
         UpdateOrigin.as_view(), name="update_origin"),
    path('supprimer-une-origine/<int:id_origin>',
         delete_origin, name="delete_origin"),
    url('creer-une-origine', CreateOrigin.as_view(), name="create_origin"),

    url('pdf-liste-des-commandes', pdf_list_command, name="pdf_list_command"),

    url('pdf-commande-globale', pdf_global_command, name="pdf_global_command"),
    url('commande-globale', global_command, name="global_command"),
]
