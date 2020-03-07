from django.urls import path, re_path, include
from django.conf.urls import url

from command.views import table_command, sommary_command, create_command, command_citrus,\
   get_citrus_list, new_command, delete_citrus_command

urlpatterns = [
   path("commander", table_command, name="command"),
   path("recapitulatif-de-la-commande", sommary_command, name='sommary_command'),
   path('nouvelle-commande', create_command, name="create_command"),
   re_path(r'^citrus-formate$', get_citrus_list),
   re_path(r'^commander-des-agrumes$', command_citrus, name='new_command_citrus'),
   re_path(r'^create-command$', new_command, name='new_command'),

   url('delete-citrus-command', delete_citrus_command)

]