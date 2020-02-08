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

from command.models import Command
from event.models import Event
from event.forms import EventForm

class CreateEvent(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "event.add_event"
    model = Event
    template_name = "event/new.html"
    form_class = EventForm
    success_url = reverse_lazy("list_event")

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, "Votre évènement a bien été enregistré.")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "Votre évènement n'a pas pu être enregistré, merci de verifier que vous avez remplis tout les champs, puis réessyaer.")
        return HttpResponseRedirect(reverse_lazy("create_event"), {"form":form})

class ListEvent(PermissionRequiredMixin, LoginRequiredMixin, ListView) :
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
        messages.warning(self.request, "Votre évènement n'a pas pu être enregistré, merci de verifier que vous avez remplis tout les champs, puis réessyaer.")
        id_event = self.kwargs.get('id_event', None)
        return HttpResponseRedirect(reverse_lazy("update_event", kwargs={"id_evenement":id_event}), {"form":form})


@permission_required("event.delete_event")
@login_required
def delete_event(request, id_event):

    event = get_object_or_404(Event, id=id_event)
    result = event.delete()
    succes_url = reverse_lazy("list_event")

    if result:
        messages.succes(request, "L'évènement a bien été supprimé.")
    else:
        messages.warning(request, "L'évènement n'a pas pu être supprimé, merci de réessayer")
    return HttpResponseRedirect(succes_url)
"""
def help_command(request):

    try:
        next_delivery = Delivery.objects.filter(Q(date__gt=timezone.now())).order_by("date")[0]
        date_limit_cc = DateLimitCC.objects.get(delivery=next_delivery)

    except IndexError:
        messages.warning(request, "Toutes les informations nessecaires au bon fonctionnement de cette partie du site n'ont\
                pas été rentrées, merci de réessayer ultérieurement")
        return HttpResponseRedirect(reverse_lazy("home"))

    except Exception:
        messages.warning(request, "Une erreur est survenue, merci de réessayer plus tard")
        return HttpResponseRedirect(reverse_lazy("home"))

    email_user_all = str()
    user = User.objects.all()

    for  u in user :
        email_user_all += u.email + " "

    if DateLimitUser.objects.filter(delivery=next_delivery):

        command = Command.objects.all()
        c = list()

        for co in command:
            c.append(("id",co.user_id))

        objects_q = [Q(x) for x in c]
        user = User.objects.exclude(reduce(operator.or_,objects_q))
        date_limit_user = DateLimitUser.objects.get(delivery=next_delivery)
        email_user = str()

        for u in user:
            email_user += u.email + " "

        data_mail_rappel = {
                "destinataire": email_user,
                "objet" : "Rappel commande d'agrumes",
                "message" : "Bonjour, il semblerai que vous n'avez toujours pas commandé d'agrumes pour la prochaine commande qui se déroulera le " + str(next_delivery.date.strftime("%d/%m/%Y")) + ", merci donc de commander avant la date limite fixée par les responsables de la commande qui est le " + str(date_limit_user.date.strftime("%d/%m/%Y")) + ". Si vous avez déjà commandé, merci de vérfier que c'est exact, puis ignoré ce message."}
        mail_rappel = MailForm(data_mail_rappel)

        data_mail_command = {
                "destinataire": email_user_all,
                "objet" : "La commande est passé",
                "message": "Bonjour, la commande vient d'être terminer. Si vous n'avez pas encore commandé, le temps est éccoulé, merci donc de ne pas commander afin de ne\
 compliquer la tâche aux responsables de la commande. La commande sera livrée le " +  str(next_delivery.date.strftime("%d/%m/%Y")) + " merci donc de vous tenir\
 disponible cette journée afin de venir chercher votre commande."}
        mail_command = MailForm(data_mail_command)

        return render(request, "help_command/help.html", locals())

    else:
        data = {
            "recipient": email_user_all,
            "subject" : "La commande d'agrumes est ouverte !",
            "message" :  \"\"\"Bonjour,

La commande de court-circuit est ouverte, merci de commander vos agrumes avant le <mettre ici la date choisi>.
Si vous avez un problème lors de la commande merci de contacter court-circuit en répondant à ce message ou adressez-vous
directement à l\'administrateur du site à l\'adresse : benhassenm@tutamail.com\"\"\"
            }
        mail_form = MailForm(data)
        date_limit_form = DateLimitUserForm()
        return render(request, "help_command/date_limit.html", locals())

def new_limit_date(request):
    next_delivery = Delivery.objects.filter(Q(date__gt=timezone.now())).order_by("date")[0]
    date_limit_cc = DateLimitCC.objects.get(delivery=next_delivery)

    if request.method == "POST":
        day = int(request.POST["jour"])
        month = int(request.POST['mois'])
        year = int(request.POST["annee"])
        date_format = date(year, month, day)

        if date_format > date_limit_cc.date:
            result = "erreur"
        else:
            date_limit = DateLimitUser()
            date_limit.date = date_format
            date_limit.delivery = next_delivery
            result = date_limit.save()

        return HttpResponse(result)

def send_mail(request):
    if request.method == "POST":
        form = MailForm()
        recipients = request.POST["recipient"]
        form.recipient = recipients.split(' ')
        form.subject = request.POST["subject"]
        form.message = request.POST['message']

        try:
            form.send_mail(request)

        except BadHeaderError:
            messages.warning(request, "Votre mail n'a pas pu être envoyé, il y a eu un problème d'entête")

        except Exception:
            messages.warning(request, "Une erreur est survenue, merci de réessayer.")
    return HttpResponseRedirect(reverse_lazy('home'))
"""
