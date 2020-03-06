from django.shortcuts import render
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import ObjectDoesNotExist
from random import random

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User

from api.serializers import CommandSerializer, AmountSerializer, ProductSerializer, UserSerializer, UserWithPermissionsSerializer
from command.models import Command, Amount, Product


class CommandViewSet(ModelViewSet):

    serializer_class = CommandSerializer
    queryset = Command.objects.all()

    def list(self, request):
        queryset = Command.objects.all()
        serializer = CommandSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        def error_response(e): return {
            'id': int(random() * 1000),
            'status': 'danger',
            'header': 'Erreur lors de l\'enregistrement de votre commande',
            'body': 'Une erreur est survenue lors de l\'enregistrement de votre commande, \
                merci de réessayer et de me contacter si vous rencontrez de nouveau cette erreur. \
                (ERREUR : {})'.format(type(e))
        }

        dict_user = request.data['user']
        try:
            user = User.objects.get(id=dict_user.get('id'))
        except (ObjectDoesNotExist, AttributeError, KeyError, Exception) as e:
            return Response(error_response(e))

        try:
            Command.objects.get(user=user)
        except ObjectDoesNotExist:
            pass
        except Exception as e:
            return Response(error_response(e))
        else:
            return Response({
                'id': int(random() * 1000),
                'status': 'warning',
                'header': 'Vous avez déjà commandé !',
                'body': 'Une commande à votre nom a déjà été trouvé ! Merci de vérifier que votre commande \
                n\'est pas déjà présente dans le tableau. Si cette commande n\'est pas de vous, merci de me contacter.'
            })

        Command.objects.create(user=user)
        return Response({
            'status': 'success',
            'header': 'Commande enregistrée',
            'body': 'Votre commande a bien été enregistré.'
        })

    def destroy(self, request, pk):
        def error_response(e): return {
            'id': int(random() * 1000),
            'status': 'danger',
            'header': 'Erreur lors de l\'enregistrement des produits de votre commande',
            'body': 'Une erreur est survenue lors de l\'enregistrement d\'un (ou plusieurs) produit⋅s, \
                merci de réessayer et de me contacter si vous rencontrez de nouveau cette erreur. \
                (ERREUR : {})'.format(e)
        }
        try:
            command = Command.objects.get(id=pk)
        except (ObjectDoesNotExist, Exception) as e:
            return Response(error_response(e))
        else:
            command.delete()
            return Response({
                'status': 'success',
                'header': 'Commande supprimée',
                'body': 'La commande de {} a bie été supprimé.'.format(command.user.username)})


class AmoutViewSet(ModelViewSet):
    serializer_class = AmountSerializer
    queryset = Amount.objects.all()

    def list(self, request):
        queryset = Amount.objects.all()
        serializer = AmountSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):

        def error_response(e): return {
            'id': int(random() * 1000),
            'status': 'danger',
            'header': 'Erreur lors de l\'enregistrement des produits de votre commande',
            'body': 'Une erreur est survenue lors de l\'enregistrement d\'un (ou plusieurs) produit⋅s, \
                merci de réessayer et de me contacter si vous rencontrez de nouveau cette erreur. \
                (ERREUR : {})'.format(type(e))
        }
       # For format data.
        amounts = dict()
        # For count number of box (maximum=6)
        total_box = float()

        # Data
        data = request.data.copy()

        try:
            user_id = data.pop('user')
        except (KeyError, Exception) as e:
            return Response(error_response(e))

        for product_id, amount in data.items():
            try:
                product = Product.objects.get(id=product_id)
                amount = float(amount)
            except (ObjectDoesNotExist, ValueError, Exception) as e:
                return Response(error_response(e))
            else:
                amounts[product.id] = (product, amount)
                if product.weight != 1:
                    total_box += amount
        try:
            assert total_box <= 6
        except AssertionError as e:
            return Response({
                'id': int(random() * 1000),
                'status': 'warning',
                'header': 'Nombre de caisse trop important',
                'header': 'Le nombre de caisse que vous avez commandé est trop important. Le nombre maximum de caisse est fixé \
                à 6 par adhérent. Merci de modifier votre commande.'
            })

        try:
            user = User.objects.get(id=user_id[0])
        except (ObjectDoesNotExist, AttributeError, KeyError, Exception) as e:
            return Response(error_response(e))

        try:
            Command.objects.get(user=user)
        except ObjectDoesNotExist:
            pass
        except Exception as e:
            return Response(error_response(e))
        else:
            return Response({
                'id': int(random() * 1000),
                'status': 'warning',
                'header': 'Vous avez déjà commandé !',
                'body': 'Une commande à votre nom a déjà été trouvé ! Merci de vérifier que votre commande \
                n\'est pas déjà présente dans le tableau. Si cette commande n\'est pas de vous, merci de me contacter.'
            })

        command = Command.objects.create(user=user)

        try:
            for product_id, data in amounts.items():
                amount = Amount.objects.create(
                    product=data[0], command=command, amount=data[1])
        except Exception as e:
            return Response(error_response(e))
        else:
            return Response({
                'status': 'success',
                'header': 'Commande enregistrée',
                'body': 'Votre commande a bien été enregistré.'
            })


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(display=True)

    def list(self, request, *args, **kwargs):
        # queryset = Product.objects.all()
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)


class CurrentUserView(APIView):
    queryset = User.objects.all()
    serializer = UserWithPermissionsSerializer()

    def get(self, request):
        serializer = UserWithPermissionsSerializer(request.user)
        return Response(serializer.data)
