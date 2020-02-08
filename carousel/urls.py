from django.conf.urls import url
from django.urls import path

from carousel.views import UpdateCarousel, delete_carousel, CreateCarousel, ListCarousel

urlpatterns = [
    url('liste-des-carousels', ListCarousel.as_view(), name="list_carousel"),
    path('modifier-un-carousel/<int:id_carousel>', UpdateCarousel.as_view(), name="update_carousel"),
    path('supprimer-un-carousel/<int:id_carousel>', delete_carousel, name="delete_carousel"),
    url('creer-un-carousel', CreateCarousel.as_view(), name="create_carousel")
]
