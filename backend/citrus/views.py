from django.dispatch import Signal, receiver
from django.shortcuts import render
from django.template.loader import get_template

from django.contrib.auth.decorators import login_required, permission_required
from django_xhtml2pdf.utils import pdf_decorator

from backend.mail import async_send_mail
from backend.citrus.models import CitrusProduct, CitrusOrder, CitrusAmount


@login_required
@permission_required('citrus.change_product', raise_exception=True)
@pdf_decorator(pdfname="recapitulatif_de_la_commande.pdf")
def sommary_orders(request):
    orders_list = dict()

    products = CitrusProduct.objects.filter(display=True)
    orders = CitrusOrder.objects.all()
    amounts = CitrusAmount.objects.all()
    total = 0

    for order in orders:
        orders_list[order.user.username] = (
            amounts.filter(order=order), order.get_price())
        total += order.get_price()
    print(orders_list)
    return render(
        request,
        "citrus/pdf/sommary_orders.html",
        {'total': round(total, 2), 'orders': orders_list, 'products': products}
    )


# Signals
# =======

citrus_order_add = Signal()


@receiver(citrus_order_add)
def send_confirm_citrus_order_mail(sender, order: CitrusOrder, create: bool = True, **kwargs) -> None:
    """
    Signal for send mail to user when he adds an citrus order.

    Parameters
    ----------
    sender: class
        Class that calls this signal.
    order : CitrusOrder
        Order saves.
    create : bool, optional
        If he is true, the order has been created.
    """
    if order.send_mail:
        html_content = get_template('citrus/mail/confirm_order.html').render({
            'order': order,
            'amounts': order.product.through.objects.filter(order=order),
            'create': create
        })

        async_send_mail('Commande confirmée', html_content, [order.user.email])
