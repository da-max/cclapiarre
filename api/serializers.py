
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, BooleanField, FloatField, RelatedField, SerializerMethodField
from command.models import Command, Amount, Product

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'last_name', 'first_name']

class ProductSerializer(ModelSerializer):
    #display = BooleanField(required=False)
    total = SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'name', 'weight', 'description', 'step', 'maximum', 'price', 'total']

    def get_total(self, product):
        return product.get_total()

class CommandSerializer(ModelSerializer):
    total = SerializerMethodField()
    user = UserSerializer()
    product = ProductSerializer(many=True)
    class Meta:
        model = Command
        fields = ['user', 'product', 'total']
    
    def get_total(self, command):
        
        return command.get_total()


class CommandSmallSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta: 
        model = Command
        fields = ['id', 'user']

class AmountSerializer(ModelSerializer):
    amount = FloatField()
    product = ProductSerializer()
    command = CommandSmallSerializer()
    class Meta:
        model = Amount
        fields = ['id', 'command', 'product', 'amount']