""" File for describes all the urls of api apps. """
from django.conf.urls import url


from rest_framework.routers import DefaultRouter

from api.views import CommandViewSet, \
 ProductViewSet, CurrentUserView, CoffeeViewSet, CommandCoffeeViewSet

urlpatterns = [
    url(r'^users/current', CurrentUserView.as_view()),
    url(r'^citrus/product\?query=all', ProductViewSet.as_view({'get': 'list_all'}))

]


ROUTER = DefaultRouter(trailing_slash=False)
ROUTER.register(r'citrus/command', CommandViewSet)
ROUTER.register(r'citrus/product', ProductViewSet, basename='product')
ROUTER.register(r'coffee/coffee', CoffeeViewSet, basename='coffee-coffee')
ROUTER.register(r'coffee/command', CommandCoffeeViewSet, basename='coffee-command-coffee')

urlpatterns += ROUTER.urls
