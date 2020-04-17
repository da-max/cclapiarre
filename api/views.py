import re
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import ObjectDoesNotExist
from random import random
from django.db.models import Q
from django.template.loader import get_template
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import m2m_changed
from django.dispatch import receiver, Signal

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from cclapiarre.exceptions import BoxNumberException
from api.serializers import CommandSerializer, AmountSerializer, ProductSerializer, UserSerializer, UserWithPermissionsSerializer, CoffeeSerializer, CommandCoffeeSerializer
from citrus.models import Command, Amount, Product
from coffee.models import Coffee, CommandCoffee, Quantity as AmountCoffee, Type
from api.pagination import StandardLimitOffsetPagination


# Created new signals
post_change_command = Signal(providing_args=['instance', 'status'])


@receiver(post_change_command, sender=Command.product.through)
def command_send_mail(sender, instance, **kwargs):
    # Send mail when command is add
    command_sommary = dict()
    if kwargs['status']:
        status = kwargs['status']

    try:
        isinstance(instance, Command)
        mail = instance.send_mail
    except Exception as e:
        return e

    if instance.send_mail:
        amounts = instance.product.through.objects.filter(command=instance)
        for amount in amounts:
            command_sommary[amount.product.name] = {
                'weight': amount.product.weight,
                'price': float(amount.product.weight * amount.amount),
                'quantity': amount.amount
            }
        SUBJECT = "Récapitulatif de votre commande"
        FROM_EMAIL = settings.DEFAULT_FROM_EMAIL
        HTML_TEXT = get_template('citrus/command_mail/sommary.html')
        PLAIN_TEXT = get_template('citrus/command_mail/sommary.txt')

        DATA = {
            'command_sommary': command_sommary,
            'first_name': instance.user.first_name,
            'email': instance.user.email,
            'total_price': Amount.get_total_user(Amount, instance.id),
            'status': status
        }

        html_content = HTML_TEXT.render(DATA)
        text_content = PLAIN_TEXT.render(DATA)
        if instance.user.email:
            send_mail(SUBJECT, text_content, FROM_EMAIL, [
                instance.user.email], html_message=html_content)


@receiver(post_change_command, sender=CommandCoffee.coffee.through)
def command_coffee_send_mail(sender, instance, **kwargs):
    command_sommary = dict()
    if kwargs['status']:
        status = kwargs['status']

    try:
        isinstance(instance, CommandCoffee)
    except Exception as e:
        return e

    amounts = instance.coffee.through.objects.filter(command=instance)
    for amount in amounts:
        command_sommary[amount.id] = {
            'farm_coop': amount.coffee.farm_coop,
            'weight': amount.weight,
            'type': amount.sort.name,
            'quantity': amount.quantity,
            'price': amount.get_price()
        }

    SUBJECT = 'Récapitulatif de votre commande de café'
    FROM_EMAIL = settings.DEFAULT_FROM_EMAIL
    HTML_TEXT = get_template('coffee/mail/command_sommary.html')
    PLAIN_TEXT = get_template('coffee/mail/command_sommary.txt')

    DATA = {
        'command_sommary': command_sommary,
        'name': instance.name,
        'first_name': instance.first_name,
        'phone_number': instance.phone_number,
        'total_price': instance.get_total_price(),
        'status': status
    }

    html_content = HTML_TEXT.render(DATA)
    text_content = PLAIN_TEXT.render(DATA)

    send_mail(SUBJECT, text_content, FROM_EMAIL, [
              instance.email], html_message=html_content)


class CommandViewSet(ModelViewSet):

    serializer_class = CommandSerializer
    queryset = Command.objects.all()

    def error_response(self, error=Exception, action="l’enregistrement"):
        return {
            'id': int(random() * 1000),
            'status': 'danger',
            'header': f'Erreur lors de {action} de la commande',
            'body': f'{error}'
        }

    def check_command(self, request):
        """ Method for check if all information send when an user command are right (this method is use when an user command or update a command). """
        BOX_LIMIT = 6
        # For count number of box (maximum=6)
        total_box = float()
        
        # For format data.
        amounts = dict()


        # Data
        data = request.data.copy()

        try:
            mail = bool(data.pop('send_mail')[0])
        except:
            # By default, a sommary mail is send.
            mail = True

        try:
            user_id = data.pop('user')[0]
            user = User.objects.get(id=user_id)
        except Exception as e:
            raise

        for product_id, amount in data.items():

            try:
                product = Product.objects.get(
                    Q(id=product_id) & Q(display=True))
                amount = float(amount)

                assert float(
                    amount % product.step) == 0

            except (AssertionError, ObjectDoesNotExist, ValueError) as e:
                raise type(e)(f"Une erreur est survenue, merci de réessayer. (ERREUR: {e})")

            else:
                if amount != float(0):
                    amounts[product.id] = {
                        'product': product,
                        'amount': amount
                        }
                    if product.weight != 1:
                        total_box += amount
        try:
            assert total_box <= BOX_LIMIT
        except AssertionError as e:
            raise BoxNumberException(f"Le nombre de caisse est limité a {BOX_LIMIT}, vous avez commandé {total_box} caisses. Merci de modifier la commande.")
        
        return (user, mail, amounts)

    def list(self, request):
        queryset = Command.objects.all()
        serializer = CommandSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):

        try:
            user, mail, amounts = self.check_command(request)
        except Exception as e:
            return Response(self.error_response(error=e))
        try:
            Command.objects.get(user__id=user.id)
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
                amount = Amount.objects.create(
                    product=data['product'], amount=data['amount'], command=command)

        except Exception as e:
            return Response(self.error_response(e))

        post_change_command.send(
            sender=Command.product.through, instance=command, status='add')
        return Response({
            'id': int(random() * 1000),
            'status': 'success',
            'header': 'Commande enregistrée',
            'body': 'Votre commande a bien été enregistrée.'
        })

    def destroy(self, request, pk):
        try:
            command = Command.objects.get(id=pk)
        except (ObjectDoesNotExist, Exception) as e:
            return Response(self.error_response(error=e, action='la suppression'))
        else:
            command.delete()
            return Response({
                'status': 'success',
                'header': 'Commande supprimée',
                'body': f'La commande de {command.user.username} a bien été supprimé.'
                })

    def update(self, request, pk):

        try:
            user, mail, amounts = self.check_command(request)
        except Exception as e:
            return Response(self.error_response(error=e, action='la modification'))

        try:
            command = Command.objects.get(Q(id=pk) & Q(user=user))
            amount = Amount.objects.filter(command=command).delete()
        except Exception as e:
            return Response(error_response(e))

        for product, amount in amounts.items():
            try:
                a = Amount.objects.create(
                    command=command, product=amount['product'], amount=amount['amount'])
            except Exception as e:
                return Response(self.error_response(e))

        post_change_command.send(
            sender=Command.product.through, instance=command, status='update')
        return Response({
            'id': int(random() * 1000),
            'status': 'success',
            'header': 'Commande modifiée',
            'body': f'La commande de {command.user.username} a bien été modifié.'
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
                'Merci de réessayer et de me contacter si besoin (ERREUR: {})'.format(
                    type(e))
            })
        else:
            return Response({
                'id': int(random() * 10000),
                'status': 'success',
                'header': 'Commandes supprimées',
                'body': 'Toutes les commandes ont bien été supprimées.'
            })


class ProductViewSet(ModelViewSet):

    serializer_class = ProductSerializer
    queryset = Product.objects.filter(display=True)
    pagination_class = StandardLimitOffsetPagination

    def get_queryset(self):
        queryset = self.queryset
        query = self.request.query_params.get('query', None)
        display = self.request.query_params.get('display', None)
        
        if query == 'all':
            queryset = Product.objects.all()
        
        if display is not None:
            queryset.filter(display=True)
        
        return queryset

    def list(self, request):
        super().list(request)
        serializer = ProductSerializer(self.get_queryset(), many=True)
        query = request.query_params.get('query', None)
        
        # If query == all I paginated_queryset and return paginated response.
        if query == 'all':
            return self.get_paginated_response(self.paginate_queryset(serializer.data))

        # Else I return classic response.
        return Response(serializer.data)

class CurrentUserView(APIView):
    queryset = User.objects.all()
    serializer = UserWithPermissionsSerializer()
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserWithPermissionsSerializer(request.user)
        return Response(serializer.data)


class CoffeeViewSet(ModelViewSet):
    serializer_class = CoffeeSerializer
    queryset = Coffee.objects.filter(display=True)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class CommandCoffeeViewSet(ModelViewSet):
    serializer_class = CommandCoffeeSerializer
    queryset = CommandCoffee.objects.all()

    def error_response(self, error=Exception, action="l’enregistrement"):
        return {
            'id': int(random() * 1000),
            'status': 'danger',
            'header': 'Erreur lors de {action} de la commande de café'.format(action=action),
            'body': str(error)
        }

    def command_check(self, request):
        """ Method for check all data send by the user when 
        he want create or update any coffeeCommand. """
        data = request.data.copy()
        personnal_data = dict()
        sommary_command = list()
        try:
            name = data.pop('name')
            first_name = data.pop('first_name')
            email = data.pop('email')
            phone_number = data.pop('phone_number')
            assert re.match('^[\w.-]+@(\w)+\.(\w){2,4}$', email)
            assert re.match('^0[0-9]([ .-]?[0-9]{2}){4}$', phone_number)
        except KeyError as key_exception:
            raise KeyError('Les champs nom, prénom, email ou numéro de télephone n’ont pas été rentrés, merci de vérifier qu’ils sont correctement renseignés, puis réessayer. (ERREUR : {})'.format(key_exception))
        except AssertionError as assertion_exception:
            raise AssertionError(
                'L’email rentré ou le numéro  de télephone n’est pas valide, merci de vérifier qu’ils sont corrects et de réessayer. (ERREUR : {})'.format(assertion_exception))
        else:
            personnal_data['name'] = name
            personnal_data['first_name'] = first_name
            personnal_data['email'] = email
            personnal_data['phone_number'] = phone_number

        for amount in data['command']:
            try:
                coffee = Coffee.objects.get(id=amount['id_coffee'])
                sort = coffee.available_type.get(
                    Q(id=amount['sort']) & Q(coffee=coffee))
                assert amount['weight'] == 200 or amount['weight'] == 1000
                assert amount['quantity'] == int(amount['quantity'])
            except ObjectDoesNotExist as object_excetion:
                raise ObjectDoesNotExist(
                    'Un ou plusieurs café commandé n’existe pas, merci de vérifier la commande, est de réessayer. (ERREUR : {})'.format(object_excetion))
            except AssertionError as assertion_exception:
                raise AssertionError(
                    'La quantité ou le poids commandé n’est pas valide, merci de vérifier la commande et de réessayer. (ERREUR : {})'.format(assertion_exception))
            except ValueError as value_exception:
                raise ValueError(
                    'Le café ou le type de mouture commandé n’existe, merci de vérifier la commande et de réessayer. (ERREUR : {})'.format(value_exception))
            except Exception as e:
                raise Exception('Erreur', e)
            else:
                sommary_command.append(
                    {
                        'coffee': coffee,
                        'sort': sort,
                        'amount': amount['quantity'],
                        'weight': amount['weight']
                    }
                )

        return (personnal_data, sommary_command)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk):
        try:
            command_coffee = CommandCoffee.objects.get(id=pk)
        except (ObjectDoesNotExist, Exception) as e:
            return Response(self.error_response(error=e, action="la suppression"))
        else:
            command_coffee.delete()
            return Response({
                'id': int(random() * 1000),
                'status': 'success',
                'header': 'Commande supprimée',
                'body': 'La commande de {} {} a bien été supprimé.'.format(command_coffee.first_name, command_coffee.name)})

    def create(self, request):

        try:
            (personnal_data, sommary_command) = self.command_check(request)
        except (ObjectDoesNotExist, KeyError, AssertionError, Exception) as e:
            return Response(self.error_response(e))

        try:
            command = CommandCoffee.objects.get(Q(email=personnal_data['email']) | Q(
                phone_number=personnal_data['phone_number']))
        except ObjectDoesNotExist:
            pass
        else:
            serializer = CommandCoffeeSerializer(command)
            return Response(({
                'status': 'also_command',
            }, serializer.data))

        command = CommandCoffee.objects.create(
            name=personnal_data['name'], first_name=personnal_data['first_name'], email=personnal_data['email'], phone_number=personnal_data['phone_number'])

        for amount in sommary_command:
            a = AmountCoffee.objects.create(
                coffee=amount['coffee'], quantity=amount['amount'], command=command, sort=amount['sort'], weight=amount['weight'])

        post_change_command.send(
            sender=CommandCoffee.coffee.through, instance=command, status='add')

        return Response({
            'id': int(random() * 1000),
            'status': 'success',
            'header': 'Commande enregistrée !',
            'body': 'Votre commande a bien été enregistré, merci d’envoyer un mail à l’adresse da-max@tutanota.com si vous souhaitez la modifier.'
        })

    def update(self, request, pk):

        try:
            command = CommandCoffee.objects.get(id=pk)
        except (ObjectDoesNotExist, Exception) as e:
            return Response(self.error_response(error=e, action='la modification'))

        try:
            (personnal_data, sommary_command) = self.command_check(request)
        except (ObjectDoesNotExist, AssertionError, Exception) as e:
            return Response(self.error_response(e))

        try:
            command = CommandCoffee.objects.get(id=pk)
            CommandCoffee.objects.filter(id=pk).update(
                name=personnal_data['name'], first_name=personnal_data['first_name'], email=personnal_data['email'], phone_number=personnal_data['phone_number'])
            command.coffee.through.objects.filter(
                command_id=command.id).delete()
        except Exception as e:
            return Response(self.error_response(error=e, action='la modification'))

        for amount in sommary_command:
            try:
                AmountCoffee.objects.create(
                    command=command, coffee=amount['coffee'], quantity=amount['amount'], weight=amount['weight'], sort=amount['sort'])
            except Exception as e:
                return Response(self.error_response(error=e, action='la modification'))

        post_change_command.send(
            sender=CommandCoffee.coffee.through, instance=command, status='update')

        return Response({
            'id': int(random() * 1000),
            'status': 'success',
            'header': 'Commande modifiée',
            'body': 'La commande de {} {} a bien été modifié.'.format(command.first_name, command.name)
        })

    @action(detail=False, methods=['delete'])
    def destroy_all(self, request):
        command = CommandCoffee.objects.all()
        try:
            command.delete()

        except Exception as e:
            return Response(self.error_response(error=e, action='la suppression'))
        else:
            return Response({
                'id': int(random() * 10000),
                'status': 'success',
                'header': 'Commandes supprimées',
                'body': 'Toutes les commandes ont bien été supprimées.'
            })
