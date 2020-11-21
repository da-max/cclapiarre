from django.conf.urls import url

from backend.application.views import pdf_list_order

urlpatterns = [
    url(r'(?P<slug_application>[a-z]*)/recapitulatif',
        pdf_list_order, name='pdf_list_oder')
]
