from django.urls import path, re_path, include
from django.conf.urls import url

from citrus.views import sommary_command, command_citrus, CitrusAppView

urlpatterns = [
   path("recapitulatif-de-la-commande", sommary_command, name='sommary_command'),
   re_path(r'^commander-des-agrumes$', command_citrus, name='new_command_citrus'),
   url(r'^liste-des-produits$', CitrusAppView.as_view(permission_required='citrus.view_product'), name='list_product'),
   url(r'^modifier-un-produit/(?P<id_product>\d{1,})', CitrusAppView.as_view(permission_required='citrus.change_product'), name='update_product')
]