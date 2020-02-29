from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import CommandSerializer, AmountSerializer, ProductSerializer, UserSerializer
from command.models import Command, Amount, Product
class CommandViewSet(ModelViewSet):

    serializer_class = CommandSerializer
    queryset = Command.objects.all()

    def list(self, request):
        queryset = Command.objects.all()
        serializer = CommandSerializer(queryset, many=True, context={'true_user': request.user})
        return Response(serializer.data)

class AmoutViewSet(ModelViewSet):
    serializer_class = AmountSerializer
    queryset = Amount.objects.all()

    def list(self, request):
        queryset = Amount.objects.all()
        serializer = AmountSerializer(queryset, many=True)
        return Response(serializer.data)

class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(display=True)
    def list(self, request, *args, **kwargs):
        #queryset = Product.objects.all()
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)

class CurrentUserView(APIView):
    serializer = UserSerializer()
    
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)