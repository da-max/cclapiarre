from django.contrib.auth.decorators import login_required, permission_required
from django.dispatch import Signal, receiver
from django.shortcuts import render, Http404
from django.template.loader import get_template
from django.template.response import TemplateResponse

from django_xhtml2pdf.utils import pdf_decorator

from backend.application.models import Application, Order
from backend.mail import async_send_mail

order_added = Signal()


@receiver(order_added)
def send_confirm_order_mail(sender, order: Order, create: bool = True, **kwargs) -> None:
    """ Signal for send mail when an order is confirm.

    Parameters
    ----------
    sender : class
        Class when the signal is called.
    order : Order
        Order saves.
    create : bool, optional
        Is True if the order has been created.
    """
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
def pdf_list_order(request, slug_application: str) -> TemplateResponse:
    """ View for generate PDF files for summarize all orders of an application.

    Parameters
    ----------
    request : Request
    slug_application : str
        slug of application to generate summarize.

    Returns
    -------
    TemplateResponse.
    """
    try:
        application_name = Application.objects.get(slug=slug_application).name
    except Application.DoesNotExist:
        raise Http404('Application non trouvée')

    orders = dict()
    try:
        order = Order.objects.filter(
            application__slug=slug_application)
    except Order.DoesNotExist:
        raise Http404('Application non trouvée.')

    for o in order:
        orders[o] = o.products.through.objects.filter(order=o)
    return render(request, 'application/pdf/list_order.html', locals())
