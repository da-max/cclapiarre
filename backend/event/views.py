import operator
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.core.mail import BadHeaderError
from django.utils import timezone
from django.http.response import HttpResponse
from django.http import Http404
from functools import reduce
from datetime import date
from django.urls.base import reverse_lazy
from django.db.models import Q
from django.views.generic import CreateView, ListView, UpdateView

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin,\
    PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import User

from backend.citrus.models import Command
from backend.event.models import Event
from backend.event.forms import EventForm


class CreateEvent(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "event.add_event"
    model = Event
    template_name = "event/new.html"
    form_class = EventForm
    success_url = reverse_lazy("list_event")

    def form_valid(self, form):
        self.object = form.save()
        messages.success(
            self.request, "Votre évènement a bien été enregistré.")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(
            self.request, "Votre évènement n'a pas pu être enregistré, merci de verifier que vous avez remplis tout les champs, puis réessyaer.")
        return HttpResponseRedirect(reverse_lazy("create_event"), {"form": form})


class ListEvent(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = "event.view_event"
    model = Event
    context_object_name = "events"
    template_name = "event/list.html"


class UpdateEvent(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = "event.change_event"
    model = Event
    template_name = "event/update.html"
    content_object_name = "event"
    success_url = reverse_lazy('list_event')
    form_class = EventForm

    def get_object(self, queryset=None):
        id = self.kwargs.get("id_event", None)
        return get_object_or_404(Event, id=id)

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, "Votre évènement a bien été modifié.")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.warning(
            self.request, "Votre évènement n'a pas pu être enregistré, merci de verifier que vous avez remplis tout les champs, puis réessyaer.")
        id_event = self.kwargs.get('id_event', None)
        return HttpResponseRedirect(reverse_lazy("update_event", kwargs={"id_evenement": id_event}), {"form": form})


@permission_required("event.delete_event")
@login_required
def delete_event(request, id_event):

    event = get_object_or_404(Event, id=id_event)
    result = event.delete()
    succes_url = reverse_lazy("list_event")

    if result:
        messages.succes(request, "L'évènement a bien été supprimé.")
    else:
        messages.warning(
            request, "L'évènement n'a pas pu être supprimé, merci de réessayer")
    return HttpResponseRedirect(succes_url)
