from django.urls import path, re_path, include
from django.conf.urls import url

from backend.citrus.views import sommary_command

urlpatterns = [
    path("recapitulatif-de-la-commande", sommary_command, name='sommary_command')
]
