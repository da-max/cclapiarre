from backend.mail import async_send_mail
from copy import deepcopy
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from django.dispatch import Signal, receiver
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.mail import mail_admins, send_mail
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import get_template

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required
from django_xhtml2pdf.utils import pdf_decorator

from backend.coffee.models import Coffee, Type, CoffeeAmount, CoffeeOrder, Origin
from backend.coffee.forms import CoffeeForm, OriginForm
from backend.registration.views import disconnection


class ListCoffee(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """ Generic class for display list of coffee, this class extends to ListView.

    permission_required -- User with permission view_coffee can view this page.
    model -- This class use Coffee model.
    context_object_name -- This class use coffees for templates.
    template_name -- This class take list.html for template.


    """

    permission_required = "coffee.view_coffee"
    model = Coffee
    context_object_name = "coffees"
    template_name = "coffee/coffee/list.html"

    def get_queryset(self):
        """ Method for personnalise request and order of data."""

        return Coffee.objects.all().order_by("region")


class CreateCoffee(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """ Generic class for create a coffee, this class extends to CreateView class.

    permission_required -- User with create_coffee can view this page.
    model -- This class use Coffee model.
    template_name -- This class take new.html template.
    form_class -- This class use CoffeeFrom class for form.
    success_url -- Success url is list of article (ListArticle class).

    form_valid -- If form is valid
    form_invalid -- If form is invalid.


    """

    permission_required = "coffee.add_coffee"
    model = Coffee
    form_class = CoffeeForm
    template_name = "coffee/coffee/new.html"
    success_url = reverse_lazy('list_coffee')

    def form_valid(self, form):
        """ If form is valid, coffee is save and
        send message for warner user.


        """
        coffees = Coffee.objects.all()
        region = form.cleaned_data['region']
        for coffee in coffees:
            if coffee.region == region:
                messages.warning(
                    self.request, "Le nom de la région du café existe déjà, merci de donner un autre nom, puis de réessayer.")
                return HttpResponseRedirect(reverse_lazy('create_coffee'), {'form': form})

        self.object = form.save()
        messages.success(self.request, "Votre café a bien été enregistré.")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """ If form is invalid, messages is send for warner user.
        And redirect to create page with form send after.


        """
        messages.warning(self.request, "Le café n'a pas pu être enregistré, merci de vérifier que vous avez remplis tout \
            les champs, que les données rentrées ne sont pas trop longues, puis réessayer.")
        return HttpResponseRedirect(reverse_lazy('create_coffee'), {"form": form})


class UpdateCoffee(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """ Generic class for update coffee.

    permission_required -- User with create_coffee can view this page.
    model -- This class use Coffee model.
    template_name -- This class take new.html template.
    form_class -- This class use CoffeeFrom class for form.
    success_url -- Success url is list of coffee (ListCoffee class).

    form_valid -- If form is valid
    form_invalid -- If form is invalid.


    """

    permission_required = "coffee.change_coffee"
    model = Coffee
    template_name = "coffee/coffee/update.html"
    content_object_name = 'coffee'
    success_url = reverse_lazy('list_coffee')
    form_class = CoffeeForm

    def get_object(self, queryset=None):
        """ This method take coffee from id.

        Key word Arguments:
            queryset {int} -- [id of coffee forYes take in database.] (default: {None})

        Return:
            [Coffee or 404] -- [Coffee object for display in update template.]


        """
        id = self.kwargs.get('id_coffee', None)
        return get_object_or_404(Coffee, id=id)

    def form_valid(self, form):

        region = form.cleaned_data['region']
        id_coffee = self.kwargs.get('id_coffee', None)
        coffees = Coffee.objects.exclude(id=id_coffee)
        for coffee in coffees:
            if coffee.region == region:
                messages.warning(self.request, "Le nom de région rentré est le même que pour un autre café, \
                    merci de le changer puis de réessayer.")
                return HttpResponseRedirect(reverse_lazy('update_coffee', kwargs={'id_coffee': id_coffee}), {'form': form})

        self.object = form.save()
        messages.success(self.request, "Le café a bien été enregistré.")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):

        id_coffee = self.kwargs.get('id_coffee', None)
        messages.warning(self.request, "Le café n'a pas pu être enregistré, merci de vérifier que vous avez remplis tout les champs\
            que les données rentrées ne sont pas trop longues, puis réessayer.")
        return HttpResponseRedirect(reverse_lazy('update_coffee', kwargs={'id_coffee': id_coffee}), {'form': form})


class ListOrigin(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """ Generic class for display list of origin, this class extends to ListView.

    permission_required -- User with permission view_coffee can view this page.
    model -- This class use Coffee model.
    context_object_name -- This class use coffees for templates.
    template_name -- This class take list.html for template.


    """

    permission_required = "coffee.view_origin"
    model = Origin
    context_object_name = "origins"
    template_name = "coffee/origin/list.html"

    def get_queryset(self):
        """ Method for personnalise request and order of data."""

        return Origin.objects.all()


class CreateOrigin(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """ Generic class for create a coffee, this class extends to CreateView class.

    permission_required -- User with create_coffee can view this page.
    model -- This class use Coffee model.
    template_name -- This class take new.html template.
    form_class -- This class use CoffeeFrom class for form.
    success_url -- Success url is list of article (ListArticle class).

    form_valid -- If form is valid
    form_invalid -- If form is invalid.


    """

    permission_required = "coffee.add_origin"
    model = Origin
    form_class = OriginForm
    template_name = "coffee/origin/new.html"
    success_url = reverse_lazy('list_origin')

    def form_valid(self, form):
        """ If form is valid, coffee is save and
        send message for warner user.


        """
        self.object = form.save()
        messages.success(self.request, "Votre origine a bien été enregistrée.")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """ If form is invalid, messages is send for warner user.
        And redirect to create page with form send after.


        """
        messages.warning(
            self.request, "L'origine n'a pas pu être enregistrée, merci de vérifier que vous avez remplis tout les champs, puis réessayer.")
        return HttpResponseRedirect(reverse_lazy('create_origin'), {"form": form})


class UpdateOrigin(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """ Generic class for update an origin.

    permission_required -- User with update_origin can view this page.
    model -- This class use Coffee model.
    template_name -- This class take new.html template.
    form_class -- This class use CoffeeFrom class for form.
    success_url -- Success url is list of coffee (ListCoffee class).

    form_valid -- If form is valid
    form_invalid -- If form is invalid.


    """

    permission_required = "coffee.change_origin"
    model = Origin
    template_name = "coffee/origin/update.html"
    content_object_name = 'origin'
    success_url = reverse_lazy('list_origin')
    form_class = OriginForm

    def get_object(self, queryset=None):
        """ This method take coffee from id.

        Key word Arguments:
            queryset {int} -- [id of coffee forYes take in database.] (default: {None})

        Return:
            [Coffee or 404] -- [Coffee object for display in update template.]


        """
        id = self.kwargs.get('id_origin', None)
        return get_object_or_404(Origin, id=id)

    def form_valid(self, form):

        id_origin = self.kwargs.get('id_origin', None)
        self.object = form.save()
        messages.success(self.request, "L'origine a bien été modifiée.")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):

        id_origin = self.kwargs.get('id_origin', None)
        messages.warning(
            self.request, "L'origine n'a pas pu être enregistré, merci de vérifier que vous avez remplis tout les champs, puis réessayer.")
        return HttpResponseRedirect(reverse_lazy('update_origin', kwargs={'id_origin': id_origin}), {'form': form})


@permission_required('coffee.delete_origin', raise_exception=True)
@login_required
def delete_origin(request, id_origin):
    """ View for delete an origin without display page."""

    origin = get_object_or_404(Origin, id=id_origin)
    result = origin.delete()
    success_url = reverse_lazy('list_origin')

    if result:
        messages.success(request, "L'origine a bien été supprimée.")
    else:
        messages.warning(
            request, "L'origine n'a pas pu être supprimée, merci de réessayer.")

    return HttpResponseRedirect(success_url)


@permission_required('coffee.delete_coffee', raise_exception=True)
@login_required
def delete_coffee(request, id_coffee):
    """ View for delte coffee without display page."""

    coffee = get_object_or_404(Coffee, id=id_coffee)
    result = coffee.delete()
    success_url = reverse_lazy('list_coffee')

    if result:
        messages.success(request, "Le café a bien été supprimé.")
    else:
        messages.warning(
            request, "Le café n'a pas pu être supprmié, merci de réessayer.")

    return HttpResponseRedirect(success_url)


@login_required
@permission_required('coffee.view_coffeeorder', raise_exception=True)
def global_command(request):

    quantitys = CoffeeAmount.objects.all()
    coffees_quantity = dict()

    for quantity in quantitys:

        metadata = (quantity.coffee, quantity.sort, quantity.weight)
        if metadata in coffees_quantity.keys():
            coffees_quantity[metadata] += quantity.quantity
        else:
            coffees_quantity[metadata] = quantity.quantity

    return render(request, "coffee/command/global_command.html", locals())

# PDF file
# ====


@login_required
@permission_required('coffee.view_coffeeorder', raise_exception=True)
@pdf_decorator(pdfname="commande_global.pdf")
def pdf_global_command(request):

    quantitys = CoffeeAmount.objects.all()
    coffees_quantity = dict()

    for quantity in quantitys:

        metadata = (quantity.coffee, quantity.sort, quantity.weight)
        if metadata in coffees_quantity.keys():
            coffees_quantity[metadata] += quantity.quantity
        else:
            coffees_quantity[metadata] = quantity.quantity

    return render(request, "coffee/pdf/global_command.html", locals())


@login_required
@permission_required('coffee.view_coffeeorder', raise_exception=True)
@pdf_decorator(pdfname="liste_des_commandes.pdf")
def pdf_list_command(request):

    orders = dict()
    order = CoffeeOrder.objects.all()
    for o in order:
        orders[o] = o.coffee.through.objects.filter(order=o)

    return render(request, "coffee/pdf/list_command.html", locals())


# Signals
# =======

coffee_order_add = Signal()


@receiver(coffee_order_add)
def send_confirm_order_mail(sender, order: CoffeeOrder, create: bool = True, **kwargs) -> None:
    """ Signal for send async mail when an coffee order is confirm.

    Parameters
    ----------
    sender : class
        Class that calls this signal.
    order : Order
        Order saves.
    create : bool, optional
        Is True if the order has been created
    """
    html_content = get_template(
        'coffee/mail/confirm_order.html'
    ).render({
        'order': order,
        'amounts': order.coffee.through.objects.filter(
            order=order
        ),
        'create': create
    })

    async_send_mail('Commande confirmée', html_content, [order.user.email])
