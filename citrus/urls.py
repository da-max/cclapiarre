from django.urls import path, re_path, include
from django.conf.urls import url

from citrus.views import sommary_command, command_citrus

urlpatterns = [
   path("recapitulatif-de-la-commande", sommary_command, name='sommary_command'),
   re_path(r'^commander-des-agrumes$', command_citrus, name='new_command_citrus'),
]