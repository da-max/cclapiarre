from django import template

register = template.Library()


@register.simple_tag(name="amount")
def amount(order, product_id):
    """
    Tags for return the amount of an order.
    """
    amount = 0

    for o in order:
        if o.product.id == product_id:
            amount = o.amount
    return amount
