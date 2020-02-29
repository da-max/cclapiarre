from django.conf.urls import url


from rest_framework.routers import DefaultRouter
from django.contrib.auth.models import User

from api.views import CommandViewSet, AmoutViewSet, ProductViewSet, CurrentUserView
from command.models import Amount, Product

urlpatterns = [
    url(r'^users/current', CurrentUserView.as_view())

]


router = DefaultRouter()
router.register(r'citrus/command', CommandViewSet)
router.register(r'^citrus/amount', AmoutViewSet, basename=Amount)
router.register(r'citrus/product', ProductViewSet, basename=Product)

urlpatterns += router.urls
