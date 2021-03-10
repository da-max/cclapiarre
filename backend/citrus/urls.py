from django.urls import path

from backend.citrus.views import sommary_orders

urlpatterns = [
    path("recapitulatif-de-la-commande", sommary_orders, name='sommary_orders')
]
