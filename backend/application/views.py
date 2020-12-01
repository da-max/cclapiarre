from django.shortcuts import render, Http404
from django.contrib.auth.decorators import login_required, permission_required

from django_xhtml2pdf.utils import pdf_decorator

from backend.application.models import Order


@login_required
@permission_required('application.view_order')
@pdf_decorator(pdfname='order.pdf')
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
