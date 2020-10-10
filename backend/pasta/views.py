from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import ListView

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django_xhtml2pdf.utils import pdf_decorator

from backend.pasta.models import Product, MetadataProduct, CommandPasta, Amount



@login_required
@permission_required('pasta.view_commandpasta', raise_exception=True)
def list_command(request):
    """ This view display list of command for each user. """
    commands = CommandPasta.objects.all()
    amounts = Amount.objects.all()
    
    data = dict()
    
    for c in commands:
        data[c] = list()
        for amount in amounts:
            if amount.command == c :
                
                data[c].append(amount)
        
    return render(request, 'pasta/command/list.html', locals())


@login_required
@permission_required('pasta.view_commandpasta', raise_exception=True)
@pdf_decorator(pdfname='liste-des-commandes-de-pâtes.pdf')
def pdf_list_command(request):
    """ PDF of list_command view. """
    commands = CommandPasta.objects.all()
    amounts = Amount.objects.all()
    
    data = dict()
    
    for c in commands:
        data[c] = list()
        for amount in amounts:
            if amount.command == c :
                
                data[c].append(amount)
        
    return render(request, 'pasta/pdf/command/list.html', locals())
    

@login_required
@permission_required('pasta.view_commandpasta', raise_exception=True)
def global_command(request):
    """ This view display command for each product (metadataproduct). """
    amounts = Amount.objects.all()
    products_amounts = dict()
    
    for amount in amounts:
        
        weight = "{} {}".format(amount.product.weight, amount.product.unit)

        metadata = (amount.product.product.name, weight)
        if metadata in products_amounts.keys():
            products_amounts[metadata] += amount.amount
        else:
            products_amounts[metadata] = amount.amount

    return render(request, 'pasta/command/global.html', locals())


@login_required
@permission_required('pasta.view_commandpasta', raise_exception=True)
@pdf_decorator(pdfname='commande-globale.pdf')
def pdf_global_command(request):
    """ PDF od global_command. """
    amounts = Amount.objects.all()
    products_amounts = dict()
    
    for amount in amounts:
        
        weight = "{} {}".format(amount.product.weight, amount.product.unit)

        metadata = (amount.product.product.name, weight)
        if metadata in products_amounts.keys():
            products_amounts[metadata] += amount.amount
        else:
            products_amounts[metadata] = amount.amount

    return render(request, 'pasta/pdf/command/global.html', locals())

@login_required
@permission_required('pasta.add_commandpasta')
def command_pasta(request):

    return render(request, 'app.html')


@login_required
@permission_required('pasta.add_commandpasta')
def get_pasta_list(request):
    """ Ajax script use by vuejs app."""

    products_list = dict()
    products = Product.objects.all()
    metadata_products = MetadataProduct.objects.filter(display=True)

    for product in products:
        available_product = dict()
        if metadata_products.filter(product=product):
            for metadata_product in metadata_products.filter(product=product):
                available_product[metadata_product.id] = {
                    'weight': metadata_product.weight,
                    'unit': metadata_product.unit.name,
                    'price': metadata_product.price,
                    'category': {
                        'name': metadata_product.category.name,
                        'description': metadata_product.category.description
                    }
                }
        products_list[product.id] = {
            'name': product.name,
            'organic_agriculture': product.organic_agriculture,
            'maximum': product.maximum,
            'available_product': available_product
        }

    return JsonResponse(products_list)


@login_required
@permission_required('pasta.add_commandpasta')
def new_command(request):
    """ Ajax call with vuejs app """

    if request.method == "POST":

        # Stock all information send by user in command variable
        command = request.POST.dict()

        products = Product.objects.all()
        metadata_products = MetadataProduct.objects.filter(display=True)

        products_list = dict()

        # verification of personnal's data send by user
        try:
            name = command.pop('name')
            first_name = command.pop('first_name')
            email = command.pop('email')
            phone_number = command.pop('phone_number')

        except KeyError:

            return JsonResponse({
                'status': 'danger',
                'header': 'Informations personnelles',
                'body': 'Les données personnelles que vous avez rentrées ne '
                    'sont pas valides, merci de les vérifier puis réessayer.'
            })

        # Check if the user haven't already command
        try:
            CommandPasta.objects.get(
                Q(email=email) | Q(phone_number=phone_number))

        except ObjectDoesNotExist:
            pass

        else:

            return JsonResponse({
                'status': 'danger',
                'header': 'Vous avez déjà commandé !',
                'body': 'Vous avez déjà commandé, si vous souhaitez modifier votre commande merci d\'envoyer un mail à: benhassenm@tutamail.com'
            })

        for product in products:
            available_product = list()
            if metadata_products.filter(product=product):
                for metadata_product in metadata_products.filter(product=product):
                    available_product.append({
                        'weight': metadata_product.weight,
                        'price': metadata_product.price
                    })

            products_list[product.name] = {
                'maximum': product.maximum,
                'available_product': available_product
            }

        command_format = dict()
        for index, metadata in command.items():
            # 0 : name \ 1 : weight \ 2 : amount
            metadata_format = metadata.split('\\')

            # Checking the lenght of metadata send
            try:
                assert len(metadata_format) == 3

            except AssertionError:

                return JsonResponse({
                    'status': 'danger',
                    'header': 'Erreur interne',
                    'body': 'Une erreur est survenue, merci d\'actualiser la page, '
                        'de recommander et de me contacter si vous rencontrez de nouveau'
                        'cette erreur (code d\'erreur: p.len).'
                })

            command_format[index] = metadata_format

        # Checking of verious informations send
        for metadata in command_format.values():

            try:
                product = metadata_products.get(
                    Q(product__name=metadata[0]) & Q(weight=metadata[1]))

            except ObjectDoesNotExist:

                return JsonResponse({
                    'status': 'danger',
                    'header': 'Produit inconnu',
                    'body': 'Le produit {} n\'est pas disponible, merci d\'actualiser la page, '
                        'de recommander et de me contacter si vous rencontrez de nouveau cette erreur.'.format(metadata[0])
                })

        # Save in database and organise data for send mail.
        command_sommary = dict()
        try:
            command = CommandPasta.objects.create(
                name=name, first_name=first_name, email=email, phone_number=phone_number)
            for index, product in command_format.items():

                p = metadata_products.get(
                    Q(product__name=product[0]) & Q(weight=product[1]))
                q = Amount.objects.create(
                    command=command, product=p, amount=product[2])
                command_sommary[index] = {
                    'name': q.product.product.name,
                    'weight': q.product.weight,
                    'amount': q.amount,
                    'price': q.get_price()
                }

        except Exception:

            return JsonResponse({
                'status': 'danger',
                'header': 'Erreur interne',
                'body': 'Votre commande n\'a pas pu être enregistrée, '
                    'merci de réesayer et de me contacter si vous '
                    'recontrez de nouveau une erreur.'
            })

        subject = 'Commande de pâtes'
        try:

            from_email = settings.DEFAULT_FROM_EMAILS
        except AttributeError:
            from_email = 'cclapiarre@zohomail.eu'

        try:

            html_text = get_template('pasta/mail/command_sommary.html')
            plain_text = get_template('pasta/mail/command_sommary.txt')

        except Exception:

            return JsonResponse({
                'status': 'primary',
                'header': 'Commande enregistrée mais ...',
                'body': 'Votre commande a bien été passée, cepedant une erreur est survenue lors de \
                    l\'envoie du mail. Merci de me contacter afin de recevoir votre mail récapitulatif.'
            })

        html_content = html_text.render({
            'command_sommary': command_sommary,
            'name': command.name,
            'first_name': command.first_name,
            'phone_number': command.phone_number,
            'total_price': command.get_total_price()
        })

        text_content = plain_text.render({
            'command_sommary': command_sommary,
            'name': command.name,
            'first_name': command.first_name,
            'phone_number': command.phone_number,
            'total_price': command.get_total_price()
        })

        try:
            send_mail(subject, text_content, from_email,
                      [email], html_message=html_content)

        except Exception:
            return JsonResponse({
                'status': 'primary',
                'header': 'Command enregistrée mais ...',
                'body': 'Votre command a bien été passée, cependant une erreur est survenue lors de \
                    l\'envoie du mail. Merci de me contacter afin de recevoir votre mail récapitulatif.'
            })

        else:

            return JsonResponse({
                'status': 'success',
                'header': 'Commande passée !',
                'body': 'Votre commande a bien été passée, un mail récapitulatif vous a été envoyé. Si vous souhaitez modifier votre commande, merci de me contacter.'
            })

    # If method is not POST
    messages.warning(request, 'La méthode utilisée afin de commander ne semble pas conforme, merci de recommander et de me contacter en cas de besoin.')
    return HttpResponseRedirect(reverse_lazy('home'))