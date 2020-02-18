from django.conf.urls import url
from django.urls import path, re_path

from coffee.views import ListCoffee, ListOrigin, UpdateOrigin, CreateOrigin, delete_origin, \
    list_command, pdf_list_command, global_command, pdf_global_command, calcul_command,\
    CreateCoffee, UpdateCoffee, delete_coffee, table_command, create_command, command_coffee,\
    get_coffees_list, new_command

urlpatterns = [
    url("liste-des-cafe", ListCoffee.as_view(), name='list_coffee'),
    url("creer-un-cafe", CreateCoffee.as_view(), name="create_coffee"),
    path('modifier-un-cafe/<int:id_coffee>', UpdateCoffee.as_view(), name='update_coffee'),
    path('supprimer-un-cafe/<int:id_coffee>', delete_coffee, name='delete_coffee'),
    url('liste-des-origines', ListOrigin.as_view(), name="list_origin"),
    path('modifier-une-origine/<int:id_origin>', UpdateOrigin.as_view(), name="update_origin"),
    path('supprimer-une-origine/<int:id_origin>', delete_origin, name="delete_origin"),
    url('creer-une-origine', CreateOrigin.as_view(), name="create_origin"),
    url('pdf-liste-des-commandes', pdf_list_command, name="pdf_list_command"),
    url(r'^liste-des-commandes$', list_command, name="list_command"),
    url('pdf-commande-globale', pdf_global_command, name="pdf_global_command"),
    url('commande-globale', global_command, name="global_command"),
    url(r'^ancien-commander-du-cafe$', table_command, name="table_command"),
    url('nouvelle-commande', create_command, name="coffee_command"),
    url('calcul-de-la-commande', calcul_command),
    url(r'^commander-du-cafe$', command_coffee, name="new_coffee_command"),
    url('coffees-formate', get_coffees_list),
    url('create-command', new_command)
]
