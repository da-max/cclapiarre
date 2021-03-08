from django.urls import path, re_path, include
from django.conf.urls import url

from backend.citrus.views import sommary_orders

urlpatterns = [
    path("recapitulatif-de-la-commande", sommary_orders, name='sommary_orders')
]
