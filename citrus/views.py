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
from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin


from citrus.models import Product, Command, Amount


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
        users.append((command.user.last_name, user_total))
        total += user_total

    for product in products:
        command_user[product.name] = []
        amouts_list[product.name] = []
        for amout in amouts.filter(product=product):
            amouts_list[product.name].append({'user': amout.command.user.username,
                                              'quantity': amout.amount})
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
@permission_required('citrus.view_product', raise_exception=True)
def command_citrus(request):
    ''' Vuejs app for command citrus.'''
    return render(request, 'app.html')

class CitrusAppView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = "app.html"