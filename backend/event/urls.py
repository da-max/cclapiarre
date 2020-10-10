from django.conf.urls import url
from django.urls import path

from backend.event.views import CreateEvent, ListEvent, delete_event, UpdateEvent

urlpatterns = [
    url('cree-un-evenement', CreateEvent.as_view(), name="create_event"),
    url('liste-des-evenements', ListEvent.as_view(), name='list_event'),
    path("supprimer-un-evement/<int:id_event>", delete_event, name="delete_event"),
    path("modifier-un-evenement/<int:id_event>", UpdateEvent.as_view(), name="update_event")
]
