import os
from random import random
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.template import Context
from django.http.response import HttpResponseRedirect
from django.template.loader import get_template
from django.conf import settings

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django_xhtml2pdf.utils import pdf_decorator


from citrus.models import Product, Command, Amount

@login_required
@permission_required('citrus.add_command', raise_exception=True)
def table_command(request):
    """ This view create a table with all commands of users,
    list of product and allows of an user to order.
    
    Arguments:
        request {request} -- [Request with Http informations.]
    
    Returns:
        [render] -- [Send informations to the template.]

    """

    products = Product.objects.filter(display=True)
    command = Command.objects.all()


    # traitement pour affichage des données :

    total_product = dict()
    total_full = float()
    total_users = dict()
    commands = dict()


    # For display total of commands

    for c in command:
        total_user = Amount.get_total_user(Amount, command_id=c.id)
        total_users[c.user] = round(total_user, 2)
        total_full += total_user

 
    # For display products with Amounts

    for p in products:
        p.step = str(p.step).replace(',', '.')
        amounts = Amount.objects.filter(product=p)
        amount = []
        am = {}
        for a in amounts:
            amount.append(a)
        for a in amount:
            am[a.command.user] = a.amount
        total = Amount.get_total_product(Amount, product=p)
        total_product[p] = [total, round(total*p.weight, 2)]
        commands[p] = am
    total_full = round(total_full, 2)

 
    # For display a warning message if user has already order.

    if request.user in total_users:
        messages.info(request, "Vous avez déjà commandé, si vous souhaitez modifier votre commande merci de contacter directement les personnes qui s'occupent de la commande, ou l'administrateur du site à cette adresse : benhassenm@tutamail.com")
 
 
    return render(request, "citrus/command/table_command.html", locals())



@login_required
@permission_required('citrus.add_command', raise_exception=True)
def create_command(request):
    """ For create an order when an user has send an order.
    
    Arguments:
        request {request} -- [Request with Http informations/]
    
    Returns:
        [HttpResponse] -- [Redirect to table of order.]


    """

    command = Command.objects.all()
    products = Product.objects.filter(display=True)

    # If user are send the form.

    if request.method == "POST":


        # For test if user has not already place an order.

        for c in command:
            if request.user == c.user:
                messages.error(request, "Vous avez déjà commandé.e, si vous voulez changer votre commande, merci de contacter le responsable de la commande !")
                return HttpResponseRedirect(reverse_lazy("command"))


        # For test if user has send good value.

        for p in products:
            if float(request.POST[p.name]) < 0:
                messages.error(request, "Une erreur s'est produite, merci de réessayer !<br> Vous avez rentrez une quantité négative pour {}, merci de vérifier puis réessayer !".format(p.name))
                return HttpResponseRedirect(reverse_lazy("command"))


        # If al is OK, create an order, and send a success message.

        command_user = Command(user=request.user, number=round(random()*1000))
        command_user.save()

        for product in products:
            if request.POST[product.name] != '' and float(request.POST[product.name]) != float(0):
                Amount(command=command_user, amount=request.POST[product.name], product=product).save()

        messages.success(request, "Votre commande a bien été prise en compte.<br> Si vous voulez modifier votre commande, merci de contacter les gérants de la commande. Pour vous déconnectez merci de cliquer <a class='uk-link' href='/acces-securiser/disconnection'>ici</a>.")
    
    else:
        messages.error(request, "Une erreur est survenue, assurez-vous de bien avoir remplis le formulaire puis réessayer.")
    
    return HttpResponseRedirect(reverse_lazy("command"))



@login_required
@permission_required('citrus.change_product', raise_exception=True)
@pdf_decorator(pdfname="recapitulatif_de_la_commande.pdf")
def sommary_command(request):
    amouts_list = dict()
    users = list()
    command_user = dict()
    products_list = dict()
    total = float()
    user_total = float()
    
    products = Product.objects.filter(display=True)
    commands = Command.objects.all()
    amouts = Amount.objects.all()
    
    for command in commands:
        
        user_total = Amount.get_total_user(Amount, command.id)
        users.append((command.user.username, user_total))
        total += user_total
    
    for product in products:
        command_user[product.name] = []
        amouts_list[product.name] = []
        for amout in amouts.filter(product=product):
            amouts_list[product.name].append({'user' : amout.command.user.username,
                                              'quantity' : amout.amount})
            command_user[product.name] += amout.command.user.username
        
        products_list[product.id] = {
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'weight': product.weight,
            'step': str(product.step).replace(',', '.'),
            'maximum': product.maximum,
            'amouts': amouts_list[product.name],
            'users': command_user,
            'total': Amount.get_total_product(Amount, product)
        }
    
    return render(request, "citrus/pdf/sommary_command.html", {'products_list': products_list, 'users': users, 'total': total})
    
@login_required
@permission_required('citrus.add_command', raise_exception=True)
def command_citrus(request):
    ''' Vuejs app for command citrus.'''
    return render(request, 'app.html')

@login_required
@permission_required('citrus.add_command', raise_exception=True)
def get_citrus_list(request):
    ''' Return list of citrus on JSON format for VueJS app. '''
    
    amouts_list = dict()
    users = list()
    command_user = dict()
    products_list = dict()
    total = float()
    user_total = float()
    
    products = Product.objects.filter(display=True)
    commands = Command.objects.all()
    amouts = Amount.objects.all()

    has_command = False
    
    for command in commands:
        
        if request.user.username == command.user.username:
            has_command = True
        
        user_total = Amount.get_total_user(Amount, command.id)
        users.append((command.user.username, user_total, command.id))
        total += user_total
    
    for product in products:
        command_user[product.name] = []
        amouts_list[product.name] = []
        for amout in amouts.filter(product=product):
            amouts_list[product.name].append({'user' : amout.command.user.username,
                                              'quantity' : amout.amount})
            command_user[product.name] += amout.command.user.username
        
        products_list[product.id] = {
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'weight': product.weight,
            'step': str(product.step).replace(',', '.'),
            'maximum': product.maximum,
            'amouts': amouts_list[product.name],
            'users': command_user,
            'total': Amount.get_total_product(Amount, product)
        }
    
    return JsonResponse({'products_list': products_list, 'users': users, 'total': total, 'has_command': has_command, 'username': request.user.username, 'email': request.user.email})


@login_required
@permission_required('citrus.delete_command', raise_exception=True)
def delete_citrus_command(request):
    """ View for delete a commandCitrus, this view is call by the VueJS app."""

    try:
        id_command = request.GET['id_command']
    except:
        return JsonResponse({
            'status': 'warning',
            'header': 'Suppression impossible !',
            'body': 'La commande séléctionné n\'a pu pu être supprimé, merci de réessayer et de me contacter si vous rencontrez de nouveau cette erreur'
        })
    print(id_command)
    command = get_object_or_404(Command, id=id_command)
    result = command.delete()

    if result:
        return JsonResponse({
            'status': 'success',
            'header': 'Commande supprimée',
            'body': 'La commande a bien été supprimé.'
        })
    else:
        return JsonResponse({
            'status':'warning',
            'header':'Erreur',
            'body': 'La commande n\'a pu être supprimé, merci de réessayer et de me contacter si vous rencontrez de nouveau cette erreur.'
        })

@login_required
@permission_required('citrus.add_command', raise_exception=True)
def new_command(request):
    """ Ajax call with vuejs app"""
    
    if request.method == 'POST':
        
        command = request.POST.dict()
        
        products = Product.objects.filter(display=True)
        
        command_user = dict()
        command_sommary = dict()
        box = float()
        
        # Check if user want receive summary mail
        try:
            bool(command['send_mail'])
        except:
            return JsonResponse({
                'id': int(random() * 1000),
                'status': 'danger',
                'header': 'Erreur',
                'body': 'Une erreur est survenue lors de l\'envoie du mail.'
            })
        else:
            if command.pop('send_mail') == 'false':
                mail = False
            else: 
                mail = True

        for product, quantity in command.items():
            
            try:
                p = products.get(name=product)
                q = float(quantity)
                assert q <= p.maximum
                
            except Product.DoesNotExist:
                
                return JsonResponse({
                    'id': int(random() * 1000),
                    'status': 'danger',
                    'header': 'Produit inconnue',
                    'body': 'Le produit {} est inconnue.'.format(product)
                    })
            
            except:
                
                return JsonResponse({
                    'id': int(random() * 1000),
                    'status': 'danger',
                    'header': 'Erreur',
                    'body': 'Une erreur est survenue, merci de réessayer et de me contacter si besoin.'
                })
        
            else:
                
                command_user[p] = q
                if (p.weight != 1):
                    box += float(command_user[p])
        
        # Check if user has not command too box of citrus (roles of association)
        try:
            assert box <= 6
        
        except AssertionError:
            
            return JsonResponse({
                'id': int(random() * 1000),
                'status': 'warning',
                'header': '<h3>Nombre de caisse trop important</h3>',
                'body': '<span class="uk-text-bold">Le nombre de caisse</span> que vous avez commandé est trop important (<span class="uk-text-bold">la quantité maximal est de 6 caisses par\
                    adhérent</span>) merci de modifier votre commande et de me contacter si vous rencontrez un problème.'
            })
        
        command = Command.objects.create(user=request.user)
        
        for product, quantity in command_user.items():
            
            command_sommary[product.name] = {
                'weight': product.weight,
                'price': float(product.weight) * float(quantity),
                'quantity': quantity
            }
            
            try:
                q = Amount.objects.create(product=product, command=command, amount=quantity)

            except:
                
                return JsonResponse({
                    'id': int(random() * 1000),
                    'status': 'danger',
                    'header': 'Erreur interne',
                    'body': 'Une erreur est survenue, merci de réessayer puis de me contacter si besoin.'
                })
            
        if mail:
                    
            subject = "Récapitulatif de la commande"
            from_mail = settings.DEFAULT_FROM_EMAIL
            html_text = get_template('citrus/command_mail/sommary.html')
            plain_text = get_template('citrus/command_mail/sommary.txt')
        
            html_content = html_text.render({
                'command_sommary': command_sommary,
                'first_name': request.user.first_name,
                'email': request.user.email,
                'total_price': Amount.get_total_user(Amount, command.id)
            })
            
            text_content = plain_text.render({
                'command_sommary': command_sommary,
                'first_name': request.user.first_name,
                'email': request.user.email,
                'total_price': Amount.get_total_user(Amount, command.id)
            })
            
            
            send_mail(subject, text_content, from_mail, [request.user.email], html_message=html_content)

            
        return JsonResponse({
            'status': 'success',
            'header': 'Commande passée',
            'body': 'Votre commande a bien été enregistrée, merci de me contacter à l\'adresse mail : da-max@tutanota.com si vous souhaitez modifier votre commande.'})