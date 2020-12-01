from django.shortcuts import render, Http404
from django.contrib.auth.decorators import login_required, permission_required
from django.dispatch import Signal, receiver
from django.template.loader import get_template

from django_xhtml2pdf.utils import pdf_decorator

from backend.mail import async_send_mail
from backend.application.models import Order

order_added = Signal()


@receiver(order_added)
def send_confirm_order_mail(sender, order, create=True, **kwargs):
    html_content = get_template(
        'application/mail/confirm_order.html').render({
            'order': order,
            'amounts': order.products.through.objects.filter(
                order=order),
            'create': create
        })
    async_send_mail('Commande confirmée', html_content, [order.user.email])


@ login_required
@ permission_required('application.view_order')
@ pdf_decorator(pdfname='order.pdf')
def pdf_list_order(request, slug_application):
    orders = dict()
    try:
        order = Order.objects.filter(
            application__slug=slug_application)
    except Order.DoesNotExist:
        raise Http404('Application non trouvée.')

    application_name = order[0].application.name

    for o in order:
        orders[o] = o.products.through.objects.filter(order=o)
    return render(request, 'application/pdf/list_order.html', locals())
