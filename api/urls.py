from django.conf.urls import url


from rest_framework.routers import DefaultRouter
from django.contrib.auth.models import User

from api.views import CommandViewSet, AmoutViewSet, ProductViewSet, CurrentUserView, CoffeeViewSet, CommandCoffeeViewSet
from citrus.models import Amount, Product

urlpatterns = [
    url(r'^users/current', CurrentUserView.as_view())

]


router = DefaultRouter(trailing_slash=False)
router.register(r'citrus/command', CommandViewSet)
router.register(r'citrus/amount', AmoutViewSet, basename='amount')
router.register(r'citrus/product', ProductViewSet, basename='product')
router.register(r'coffee/coffee', CoffeeViewSet, basename='coffee-coffee')
router.register(r'coffee/command', CommandCoffeeViewSet, basename='coffee-command-coffee')

urlpatterns += router.urls
