from django.shortcuts import render, get_object_or_404
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import ObjectDoesNotExist
from random import random
from django.db.models import Q
from django.template.loader import get_template
from django.conf import settings
from django.core.mail import send_mail

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
            'header': 'Erreur lors de l\'enregistrement des produits de votre commande',
            'body': 'Une erreur est survenue lors de l\'enregistrement d\'un (ou plusieurs) produit⋅s, \
                merci de réessayer et de me contacter si vous rencontrez de nouveau cette erreur. \
                (ERREUR : {})'.format(type(e))
        }
       # For format data.
        amounts = dict()

        # For send mail
        command_sommary = dict()
        # For count number of box (maximum=6)
        total_box = float()

        # Data
        data = request.data.copy()

        try:
            user_id = data.pop('user')
            mail = data.pop('send_mail')
        except (KeyError, Exception) as e:
            return Response(error_response(e))

        for product_id, amount in data.items():
            try:
                product = Product.objects.get(Q(id=product_id) & Q(display=True))
                amount = float(amount)
                assert float(
                    amount % product.step) == 0
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
                'body': 'Le nombre de caisse que vous avez commandé est trop important. '
                'Le nombre maximum de caisse est fixé à 6 par adhérent. Merci de modifier votre commande.'
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
                'body': 'Une commande à votre nom a déjà été trouvé ! Merci de vérifier que votre commande '
                'n\'est pas déjà présente dans le tableau. Si cette commande n\'est pas de vous, merci de me contacter.'
            })

        command = Command.objects.create(user=user)

        try:
            for product_id, data in amounts.items():
                command_sommary[data[0].name] = {
                    'weight': data[0].name,
                    'price': float(data[0].weight) * float(data[1]),
                    'quantity': data[1]
                }
                amount = Amount.objects.create(
                    product=data[0], command=command, amount=data[1])
        except Exception as e:
            return Response(error_response(e))
        else:
            if mail:
                subject = "Récapitulatif de la commande"
                from_mail = settings.DEFAULT_FROM_EMAIL
                html_text = get_template('command/command_mail/sommary.html')
                plain_text = get_template('command/command_mail/sommary.txt')

                html_content = html_text.render({
                    'command_sommary': command_sommary,
                    'first_name': request.user.first_name,
                    'email': request.user.email,
                    'total_price': Amount.get_total_user(Amount, command.id)
                })

                text_content = plain_text.render({
                    'command_sommary': command_sommary,
                    'first_name': request.user.first_name,
                    'email': request.user.email,
                    'total_price': Amount.get_total_user(Amount, command.id)
                })

                send_mail(subject, text_content, from_mail, [
                          request.user.email], html_message=html_content)

            return Response({
                'id': int(random() * 1000),
                'status': 'success',
                'header': 'Commande enregistrée',
                'body': 'Votre commande a bien été enregistrée.'
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

    def update(self, request, pk):
        def error_response(e): return {
            'id': int(random() * 1000),
            'status': 'danger',
            'header': 'Erreur lors de la modification de la commande',
            'body': 'Une erreur est survenue lors de la modification de la commande'
                'merci de réessayer et de me contacter si vous rencontrez de nouveau cette erreur. '
                '(ERREUR : {})'.format(type(e))
        }
        amounts = dict()
        data = request.data.copy()
        total_box = float()
        try:
            user_id = data.pop('user_id')[0]
            command = Command.objects.get(Q(id=pk) & Q(user_id=user_id))
            amount = Amount.objects.filter(command=command).delete()
        except Exception as e:
            return Response(error_response(e))

        for product_id, amount in data.items():
            try:
                product = Product.objects.get(Q(id=product_id) & Q(display=True))
                amount = float(amount)
                assert float(
                    amount % product.step) == 0
            except (ObjectDoesNotExist, Exception) as e:
                return Response(error_response(e))
            else:
                if product.weight != 1:
                    total_box += amount
                amounts[product] = amount
        try:
            assert total_box <= 6
        except AssertionError as e:
            return Response({
                'id': int(random() * 1000),
                'status': 'warning',
                'header': 'Nombre de caisse trop important',
                'body': 'Le nombre de caisse commandé est trop important. '
                'Le nombre maximum de caisse est fixé à 6 par adhérent. Merci de modifier la commande.'
            })

        for product, amount in amounts.items():
            try:
                a = Amount.objects.create(
                    command=command, product=product, amount=amount)
            except Exception as e:
                return Response(error_response(e))

        return Response({
            'id': int(random() * 1000),
            'status': 'success',
            'header': 'Commande modifiée',
            'body': 'La commande de {} a bien été modifié.'.format(command.user.username)
        })


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
