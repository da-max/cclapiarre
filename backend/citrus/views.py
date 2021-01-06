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


from backend.citrus.models import CitrusProduct, CitrusOrder, CitrusAmount


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

    products = CitrusProduct.objects.filter(display=True)
    commands = CitrusOrder.objects.all()
    amouts = CitrusAmount.objects.all()

    for command in commands:

        user_total = CitrusAmount.get_total_user(CitrusAmount, command.id)
        users.append((command.user.username, user_total))
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
            'total': CitrusAmount.get_total_product(CitrusAmount, product)
        }

    return render(request, "citrus/pdf/sommary_command.html", {'products_list': products_list, 'users': users, 'total': total})
