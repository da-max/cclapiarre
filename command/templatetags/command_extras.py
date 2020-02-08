from django import template

register = template.Library()

@register.simple_tag(name='quantity')
def quantity(user, amouts_users):

    for amout in amouts_users:
        if user == amout['user']:
            return amout['quantity']
    return 0