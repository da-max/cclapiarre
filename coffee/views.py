from copy import deepcopy
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
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

from coffee.models import Coffee, Type, CommandCoffee, Quantity, Origin
from coffee.forms import CoffeeForm, OriginForm
from registration.views import disconnection


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
                messages.warning(self.request, "Le nom de région que rentré est le même que pour un autre café, \
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


@permission_required('coffee.delete_commandcoffee', raise_exception=True)
@login_required
def delete_command(request, id_command):

    command = get_object_or_404(CommandCoffee, id=id_command)
    result = command.delete()

    if result:
        messages.success(request, "La commande a bien été supprimé.")
    else:
        messages.warning(
            request, "La commande séléctionnée n'a pas pu être supprimé, merci de réessayer")

    return HttpResponseRedirect(reverse_lazy('list_command'))


@permission_required('coffee.delete_commandcoffee', raise_exception=True)
@login_required
def delete_all_command_coffee(request):
    command_coffee = CommandCoffee.objects.all()
    result = command_coffee.delete()

    if result:
        messages.success(request, "Toutes les commandes ont été supprimé.")
    else:
        messages.warning(
            request, "Les commandes n'ont pas pu être supprimé, merci de réessayer.")

    return HttpResponseRedirect(reverse_lazy('list_command'))


@login_required
@permission_required('coffee.can_commandcoffee', raise_exception=True)
def table_command(request):
    """



    """
    coffees_type = dict()  # For list type available for coffee

    coffees = Coffee.objects.filter(display=True)
    types = Type.objects.all()
    for coffee in coffees:
        type_available = list()
        for t in coffee.available_type.all():
            type_available.append(t.name)
        coffees_type[coffee] = type_available

    return render(request, 'coffee/coffee/table_command.html', locals())


@permission_required('coffee.can_commandcoffee', raise_exception=True)
@login_required
def calcul_command(request):
    """
        This script is use with AJAX for calcul total of command without save in database.

    """
    coffees = Coffee.objects.filter(display=True)
    sorts = Type.objects.all()

    id_coffees = dict()
    post = deepcopy(request.POST)
    coffee_price = dict()
    id_sort = dict()
    total_price = int(0)
    result = dict()
    n = int(0)

    if post['name'] and post['first_name'] and post['email']:

        name = result['name'] = str(post['name'])
        first_name = result['first_name'] = str(post['first_name'])
        email = result['email'] = str(post['email'])

    else:

        result['retour'] = "Info"
        return JsonResponse(result)

    del post['csrfmiddlewaretoken'], post['email'], post['name'], post['first_name']

    for coffee in coffees:
        id_coffees[coffee.id] = coffee

    for sort in sorts:
        id_sort[sort.id] = sort.name

    for coffee, quantity in post.items():
        metadata = coffee.split("/")
        if len(metadata) != 3:
            mail_admins(
                "Tableau trop long (ou trop court).",
                "Une erreur est survenue lors de la commande de {} - {} avec l'adresse mail {}, le tableau qui a été passé en paramètre contient {} valeur (normalement il est sensé y en avoir 3) !".format(
                    name, first_name, email, len(metadata))
            )
            result['retour'] = False
            return JsonResponse(result)

        if quantity != 0 and quantity != '':
            try:
                int(quantity)
                if int(quantity) < 0:
                    raise ValueError

            except ValueError:
                result['retour'] = "Nb"
                return JsonResponse(result)

            try:
                c = id_coffees[int(metadata[0])]
                s = id_sort[int(metadata[2])]
            except KeyError:
                mail_admins(
                    "Id inconnue.",
                    "Une erreur est survenue lors de la commande de {} - {} avec l'adresse mail {}, le café portant l'id : {} n'existe pas/ ou l'id du type qui est {}, mais il a été passé en paramètre.".format(
                        name, first_name, email, metadata[0], metadata[2])
                )
                result['retour'] = False
                return JsonResponse(result)

            if int(metadata[1]) == 200:
                coffee_price[c] = (int(quantity), int(
                    quantity) * c.two_hundred_gram_price)
                result[n] = [c.farm_coop, 200, s, quantity,
                             int(quantity) * c.two_hundred_gram_price]
            elif int(metadata[1]) == 1000:
                result[n] = [c.farm_coop, 1000, s, quantity,
                             int(quantity) * c.kilogram_price]
                coffee_price[c] = (int(quantity), int(
                    quantity) * c.kilogram_price)
            else:
                mail_admins(
                    "Quantité inconnue.",
                    "Une erreur est survenue lors de la commande de {} - {} avec l'adresse mail {}, a envoyé un café avec l'id : {} et une quantité de {}.".format(
                        name, first_name, email, metadata[0], metadata[1])
                )
                result['retour'] = False
                return JsonResponse(result)
            n += 1
            price = coffee_price[c]
            total_price += float(price[1])

    result['total'] = total_price

    return JsonResponse(result)


@login_required
@permission_required('coffee.can_commandcoffee', raise_exception=True)
def create_command(request):

    coffees = Coffee.objects.filter(display=True)
    commands = CommandCoffee.objects.all()
    types = Type.objects.all()

    coffees_type = dict()  # For list type available for coffee
    post = deepcopy(request.POST)
    command_sommary = str()  # For send mail with sommary of command without html
    command_sommary_html = str()  # For send mail with sommary of command with html

    if 'name' not in request.POST or 'first_name' not in request.POST or 'email' not in request.POST:
        messages.warning(request, "Les champs prénom, nom et email sont obligatoires, merci de bien vouloir les remplir.\
            Ces données ne sont en aucun cas utilisé pour d'autre objectif que de vous contacter et de\
                vérifier que vous ne commandez pas plusieurs fois.")
        return HttpResponseRedirect(reverse_lazy('table_command'))

    email = str(post["email"])
    name = str(post["name"])
    first_name = str(post["first_name"])

    del post["csrfmiddlewaretoken"], post['email'], post["name"], post["first_name"]

    # Pour vérifier que l'adresse mail ou le nom n'a pas déjà été rentrée.
    for command in commands:
        if command.email == email or command.name == name:
            messages.warning(request, "Une autre commande a été passé avec le même nom ou la même adresse mail.<br>\
                    Une seule commande est autorisée par adhérent, merci de contacter l'administrateur du site (à l'adresse benhassenm@tutamail.com) si vous souhaitez modifier votre commande.")
            return HttpResponseRedirect(reverse_lazy('table_command'))

    command_user = CommandCoffee(name=name, first_name=first_name, email=email)
    coffees_user = dict()

    # For list all type and coffee available
    for coffee in coffees:
        type_available = list()
        for t in coffee.available_type.all():
            type_available.append(t.id)
        coffees_type[coffee.id] = type_available

    command_user.save()

    # For organise all data
    for key, value in post.items():
        tab = list()
        tab = key.split('/')
        if len(tab) != 3:
            messages.error(
                request, "Une erreur est survenue, merci de réssayer. Un rapport d'erreur a été envoyé automatiquement.")
            mail_admins(
                "Tableau trop long (ou trop court)",
                "Une erreur est survenue lors de la commande de {} - {} avec l'adresse mail {}, le tableau qui a été passé en paramètre contient {} valeur (normalement il est sensé y en avoir 3) !".format(name, first_name, email, len(tab)))
            return HttpResponseRedirect(reverse_lazy('table_command'))

        if value != '' and value != 0:

            try:
                int(value)
                if int(value) < 0:
                    raise ValueError

            except ValueError:
                messages.error(
                    "Une erreur est survenue, merci de vérifier que vous avez bien rentré uniquement des nombres entiers et positifs.")
                return HttpResponseRedirect(reverse_lazy('table_command'))

            id_coffee = int(tab[0])
            weight = int(tab[1])
            id_type = int(tab[2])
            # print(coffees_type)
            # print(tab)
            if id_coffee not in coffees_type.keys() or id_type not in coffees_type[id_coffee]:
                messages.error(
                    request, "Une erreur est survenue, merci de réssayer ! <span class='uk-text-bold'>Un café commandé n'existe pas</span>.")
                mail_admins(
                    "Le café n'existe pas",
                    "Le café portant l'id {} avec le type d'id {} n'a pas été trouvé. Cette erreur est survenue lors de la commande de {} - {} avec l'adresse mail {}.".format(
                        id_type, id_type, name, first_name, email)
                )
                return HttpResponseRedirect(reverse_lazy('table_command'))

            sort = Type.objects.get(id=id_type)
            cof = Coffee.objects.get(id=id_coffee)
            q = Quantity(coffee=cof, command=command_user,
                         quantity=value, weight=weight, sort=sort)
            q.save()
            command_sommary += "{} ({}) ............... {} x {} = {} €\n".format(
                cof.farm_coop, sort.name, weight, value, q.get_price())

    subject = "Commande de café"
    from_email = "cclapiarre@zohomail.eu"
    command_sommary += "total ............... {} €\n".format(
        command_user.get_total_price())
    footer_mail = "Ce mail a été envoyé automatiquement, si vous avez des questions ou si vous souhaitez modifier votre commande, vous pouvez répondre directement à ce mail."
    text_mail = "Vous venez de commander des cafés sur le site cclapiarre.deblan.fr. Voici donc un récapitulatif de votre commande.\
        N'oubliez pas de venir chercher votre commande lors du prochain panier.\n\n{}\n\n{}".format(command_sommary, footer_mail)

    mail = send_mail(subject, text_mail, from_email, [email])

    messages.success(
        request, "Votre commande a bien été enregistrée ! Pour vous déconnectez merci de cliquer <a class='uk-link' href='/acces-securiser/disconnection'>ici</a>.")

    return HttpResponseRedirect(reverse_lazy('table_command'))


@login_required
@permission_required('coffee.view_commandcoffee', raise_exception=True)
def global_command(request):

    quantitys = Quantity.objects.all()
    coffees_quantity = dict()

    for quantity in quantitys:

        metadata = (quantity.coffee, quantity.sort, quantity.weight)
        if metadata in coffees_quantity.keys():
            coffees_quantity[metadata] += quantity.quantity
        else:
            coffees_quantity[metadata] = quantity.quantity

    return render(request, "coffee/command/global_command.html", locals())


@login_required
@permission_required('coffee.view_commandcoffee', raise_exception=True)
@pdf_decorator(pdfname="commande_global.pdf")
def pdf_global_command(request):

    quantitys = Quantity.objects.all()
    coffees_quantity = dict()

    for quantity in quantitys:

        metadata = (quantity.coffee, quantity.sort, quantity.weight)
        if metadata in coffees_quantity.keys():
            coffees_quantity[metadata] += quantity.quantity
        else:
            coffees_quantity[metadata] = quantity.quantity

    return render(request, "coffee/pdf/global_command.html", locals())


@login_required
@permission_required('coffee.view_commandcoffee', raise_exception=True)
def list_command(request):

    commands = CommandCoffee.objects.all()
    quantitys = Quantity.objects.all()

    data = dict()

    for command in commands:

        data[command] = list()
        for quantity in quantitys:

            if quantity.command == command:

                data[command].append(quantity)

    return render(request, "coffee/command/list_command.html", locals())


@login_required
@permission_required('coffee.view_commandcoffee', raise_exception=True)
@pdf_decorator(pdfname="liste_des_commandes.pdf")
def pdf_list_command(request):

    commands = CommandCoffee.objects.all()
    quantitys = Quantity.objects.all()

    data = dict()

    for command in commands:

        data[command] = []
        for quantity in quantitys:

            if quantity.command == command:

                data[command].append(quantity)

    return render(request, "coffee/pdf/list_command.html", locals())


@login_required
@permission_required('coffee.add_commandcoffee', raise_exception=True)
def command_coffee(request):

    return render(request, "app.html")


@login_required
@permission_required('coffee.add_commandcoffee', raise_exception=True)
def get_coffees_list(request):
    """Ajax script use with vuejs app"""

    coffees_list = dict()
    coffees = Coffee.objects.filter(display=True)
    for coffee in coffees:
        available_type = dict()
        for t in coffee.available_type.all():
            available_type[t.id] = t.name
        coffees_list[coffee.id] = {
            'farm_coop': coffee.farm_coop,
            'origin': coffee.origin.name,
            'maximum': coffee.maximum,
            'region': coffee.region,
            'description': coffee.description,
            'process': coffee.process,
            'variety': coffee.variety,
            'two_hundred_gram_price': coffee.two_hundred_gram_price,
            'kilogram_price': coffee.kilogram_price,
            'available_type': available_type
        }
    return JsonResponse(coffees_list)


@login_required
@permission_required('coffee.add_commandcoffee', raise_exception=True)
def new_command(request):
    """ Ajax call with vuejs app"""

    if request.method == "POST":

        # print(request.POST.dict())
        command = request.POST.dict()
        coffees = Coffee.objects.filter(display=True)
        coffees_format = dict()

        # Format available coffee from database
        for coffee in coffees:
            available_type = list()
            for t in coffee.available_type.all():
                available_type.append(t.name)

            coffees_format[coffee.farm_coop] = available_type

        # verification of personal's information send by user
        try:
            name = command['name']
            first_name = command['first_name']
            email = command['email']
            phone_number = command['phone_number']

        except KeyError:

            return JsonResponse({'status_code': 'danger',
                                 'header': 'Informations personnelles',
                                 'body': 'Les données personnelles que vous avez rentrées ne sont pas valides merci de les vérifier puis de réessayer.'
                                 })

        else:

            del command['name'], command['first_name'], command['email'], command['phone_number']

        # Check if an user haven't already command
        try:
            CommandCoffee.objects.get(Q(name=name) | Q(email=email))
        except ObjectDoesNotExist:
            pass

        else:
            return JsonResponse({'status_code': 'danger',
                                 'header': 'Vous avez déjà commandé !',
                                 'body': "Vous avez déjà commandé, si vous souhaitez modifier votre commande merci d'envoyer un mail à : benhassenm@tutamail.com"
                                 })
        # Format metadata of coffee
        command_format = dict()
        for index, metadata in command.items():
            # 0 : farm_coop / 1 : weight / 2 : type / 3 : quantity
            metadata_format = metadata.split('/')

            # checking the length of list
            if len(metadata_format) != 4:

                return JsonResponse({'status_code': 'danger',
                                     'header': 'Erreur interne',
                                     'body': "Une erreur est survenue merci d'actualiser la page, "
                                     "de recommander et de me contacter si vous rencontrez de nouveau cette erreur."
                                     })

            command_format[index] = metadata_format

        # Verification of different parameters send
        for coffee in command_format.values():

            if coffee[0] not in coffees_format.keys():

                return JsonResponse({'status_code': 'danger',
                                     'header': 'Café inconnu',
                                     'body': "Les café {} n'est pas disponible, merci d'actualiser la page "
                                     "puis de me contacter si vous rencontrez de nouveau cette erreur.".format(
                                         coffee[0])
                                     })

            if coffee[1] != '200 grammes' and coffee[1] != '1 kg':

                return JsonResponse({'status_code': 'danger',
                                     'header': 'Poids inconnu',
                                     'body': "Le poids que vous avez sélectionné pour le café {} n'est pas disponible merci d'actualiser "
                                     "la page de recommander et de me contacter si vous rencontrez de nouveau cette erreur.".format(coffee[0])})

            if coffee[2] not in coffees_format[coffee[0]]:

                return JsonResponse({'status_code': 'danger',
                                     'header': 'Type non disponible !',
                                     'body': "Le type que vous avez sélectionné pour le café {} n'est pas disponible, "
                                     "merci d'actualiser la page puis recommander et de me contacter si vous rencontrez de nouveau cette erreur.".format(coffee[0])})

        # Save in database and organise data for send mail.
        command_sommary = dict()
        try:
            command = CommandCoffee.objects.create(
                name=name, first_name=first_name, email=email, phone_number=phone_number)
            for id, com in command_format.items():

                c = Coffee.objects.get(farm_coop=com[0])
                t = Type.objects.get(name=com[2])
                if com[1] == '200 grammes':
                    q = Quantity.objects.create(
                        coffee=c, command=command, quantity=int(com[3]), weight=200, sort=t)
                elif com[1] == '1 kg':
                    q = Quantity.objects.create(
                        coffee=c, command=command, quantity=int(com[3]), weight=1000, sort=t)

                command_sommary[id] = {
                    'farm_coop': com[0],
                    'weight': com[1],
                    'type': com[2],
                    'quantity': com[3],
                    'price': q.get_price()
                }

        except:

            return JsonResponse({'status_code': 'danger',
                                 'header': 'Erreur interne',
                                 'body': "Votre commande n'a pas pu être enregistré pour une erreur inconnue, merci de réessayer "
                                 "et de me contacter si vous rencontrez de nouveau cette erreur."})
        else:

            subject = "Commande de café"
            from_email = 'cclapiarre@zohomail.eu'
            html_text = get_template('coffee/mail/command_sommary.html')
            plain_text = get_template('coffee/mail/command_sommary.txt')

            html_content = html_text.render({
                'command_sommary': command_sommary,
                'name': name,
                'first_name': first_name,
                'phone_number': phone_number,
                'total_price': command.get_total_price()
            })

            text_content = plain_text.render({
                'command_sommary': command_sommary,
                'name': name,
                'first_name': first_name,
                'phone_number': phone_number,
                'total_price': command.get_total_price()
            })

            send_mail(subject, text_content, from_email,
                      [email], html_message=html_content)

            return JsonResponse({'status_code': 'success', 'header': 'oui'})

    else:
        messages.warning(request, "La méthode utilisée afin de commander ne semble pas conforme, merci de recommander "
                         "et de me contacter en cas de besoin.")
        return HttpResponseRedirect(reverse_lazy('home'))
