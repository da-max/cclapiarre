from django.shortcuts import render, get_object_or_404
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import ObjectDoesNotExist
from random import random
from django.db.models import Q
from django.template.loader import get_template
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.decorators import action

from api.serializers import CommandSerializer, AmountSerializer, ProductSerializer, UserSerializer, UserWithPermissionsSerializer
from command.models import Command, Amount, Product


@receiver(m2m_changed, sender=Command.product.through)
def command_send_mail(sender, instance, action, **kwargs):

    # Send mail when command is add
    if action == 'post_add':
        command_sommary = dict()
        try:
            isinstance(instance, Command)
            mail = instance.send_mail
        except Exception as e:
            return e

        if instance.send_mail:
            amounts = instance.product.through.objects.all()
            for amount in amounts:
                command_sommary[amount.product.name] = {
                    'weight': amount.product.weight,
                    'price': float(amount.product.weight * amount.amount),
                    'quantity': amount.amount
                }
            SUBJECT = "Récapitulatif de la commande"
            FROM_EMAIL = settings.DEFAULT_FROM_EMAIL
            HTML_TEXT = get_template('command/command_mail/sommary.html')
            PLAIN_TEXT = get_template('command/command_mail/sommary.txt')

            DATA = {
                'command_sommary': command_sommary,
                'first_name': instance.user.first_name,
                'email': instance.user.email,
                'total_price': Amount.get_total_user(Amount, instance.id)
            }

            html_content = HTML_TEXT.render(DATA)
            text_content = PLAIN_TEXT.render(DATA)
            send_mail(SUBJECT, text_content, FROM_EMAIL, [
                instance.user.email], html_message=html_content)


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
            mail = bool(int(data.pop('send_mail')[0]))
        except (KeyError, Exception) as e:
            return Response(error_response(e))

        for product_id, amount in data.items():

            try:
                product = Product.objects.get(
                    Q(id=product_id) & Q(display=True))
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

        try:
            command = Command.objects.create(user=user, send_mail=mail)

            for product_id, data in amounts.items():
                product = data[0]
                amount = data[1]
                try:
                    assert float(amount) != float(0)
                except:
                    pass
                else:
                    amount = Amount.objects.create(
                        product=product, amount=amount, command=command)
                    command.product.add(data[0], through_defaults=amount)
        
        except Exception as e:
            return Response(error_response(e))

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
                product = Product.objects.get(
                    Q(id=product_id) & Q(display=True))
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
                command.product.add(product, through_defaults=a)
            except Exception as e:
                return Response(error_response(e))

        return Response({
            'id': int(random() * 1000),
            'status': 'success',
            'header': 'Commande modifiée',
            'body': 'La commande de {} a bien été modifié.'.format(command.user.username)
        })

    @action(detail=False, methods=['delete'])
    def destroy_all(self, request):
        command = Command.objects.all()
        try:
            command.delete()
            
        except Exception as e:
            return Response({
                'id': int(random() * 10000),
                'status': 'danger',
                'header': 'Erreur interne',
                'body': 'Une erreur est survenue lors de la suppression de toutes les commandes. '
                'Merce de réessayer et de me contacter si besoin (ERREUR: {})'.format(type(e))
            })
        else:
            return Response({
                'id': int(random() * 10000),
                'status': 'success',
                'header': 'Commandes supprimées',
                'body': 'Toutes les commandes ont bien été supprimées.'
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
                    product=data[0], amount=data[1])
                command.product.add(amount)
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
