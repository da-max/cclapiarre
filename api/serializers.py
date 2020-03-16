
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, BooleanField, FloatField, RelatedField, SerializerMethodField

from command.models import Command, Amount, Product
from coffee.models import Origin as CoffeeOrigin, Quantity as CoffeeAmount, Coffee, CommandCoffee, Type as CoffeeType


class UserWithPermissionsSerializer(ModelSerializer):
    permissions = SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'last_name', 'first_name', 'permissions']

    def get_permissions(self, user):
        return user.get_all_permissions()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'last_name', 'first_name']


class ProductSerializer(ModelSerializer):
    #display = BooleanField(required=False)
    total = SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'weight', 'description',
                  'step', 'maximum', 'price', 'total']

    def get_total(self, product):
        return product.get_total()


class CommandSerializer(ModelSerializer):
    total = SerializerMethodField()
    user = UserSerializer()
    product = ProductSerializer(many=True)

    class Meta:
        model = Command
        fields = ['user', 'product', 'total', 'id']

    def get_total(self, command):

        return command.get_total()


class CommandSmallSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Command
        fields = ['id', 'user']


class AmountSerializer(RelatedField):
    amount = FloatField()
    product = ProductSerializer()
    command = CommandSmallSerializer()

    class Meta:
        model = Amount
        fields = ['id', 'command', 'product', 'amount']


""" Serializer for coffee app """


class OriginSerializer(ModelSerializer):
    class Meta:
        model = CoffeeOrigin
        fields = ['id', 'name']


class AvailableTypeSerializer(ModelSerializer):
    class Meta:
        model = CoffeeType
        fields = ['id', 'name']


class CoffeeSerializer(ModelSerializer):
    origin = OriginSerializer()
    available_type = AvailableTypeSerializer(many=True)

    class Meta:
        model = Coffee
        fields = ['id', 'origin', 'farm_coop', 'region', 'description',
                  'process', 'variety', 'two_hundred_gram_price', 'kilogram_price', 'maximum', 'available_type']


class AmountCoffeeSerializer(ModelSerializer):
    
    coffee = CoffeeSerializer()
    sort = AvailableTypeSerializer()
    class Meta:
        model = CoffeeAmount
        fields = ['id', 'quantity', 'sort', 'coffee']

class CommandCoffeeSerializer(ModelSerializer):
    #coffee.amount = AmountCoffeeSerializer(many=True)
    command = AmountCoffeeSerializer(many=True)
    class Meta:
        model = CommandCoffee
        fields = ['id', 'name', 'first_name', 'email', 'phone_number', 'command']