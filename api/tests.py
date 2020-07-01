import json
from random import random
from django.urls import reverse, path, include
from django.db.models import ObjectDoesNotExist

from rest_framework.test import APITransactionTestCase, URLPatternsTestCase, APIClient, APIRequestFactory
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import User

from citrus.models import Amount, Product, Command
from coffee.models import Coffee, CommandCoffee, Quantity as AmountCoffee, Origin as OriginCoffee, Type as TypeCoffee
from registration.views import connect


class CommandApiTestCase (APITransactionTestCase, URLPatternsTestCase):

    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    def setUp(self):
        self.super_user = User.objects.create_superuser(
            'test1', 'test1@test.com', 'password')
        self.user = User.objects.create(
            username='user1', email='user1@user.com', password='password')

        user_logged_in.disconnect(receiver=connect)


class CitrusApiTestCase (CommandApiTestCase):
    """ This class user APITransactioTestCase and URLPatternsTestCase for use urlpatterns attribut
    So this class depends to rest_framework module.
    The client is define in setUp method, this client is APIClient."""

    def setUp(self):
        """ Define user, command and product for all CitrusApiTestCase. 

        super_user is client of Test with all permissions (permissions are tests later).
        a command is save with super_user for user, this command is update in test_*_*_*_update_command tests.
        a user self.user is than command on test_*_*_*_add_command tests.
        p3 product is o product with display=False, it is impossibel to command this product.
        p2 is sole product with width != 1 so just him counts in numver_case variable, it's also this product 
        who have specify step (this is test).

        two error_response is define : add_error_response is the error_response of create mzthod
        of CommandViewSet class.
        update_error_response is the error_response of update method of CommandViewSet class.


        """
        super().setUp()
        self.add_error_response = lambda id, e: {
            'id': id,
            'status': 'danger',
            'header': 'Erreur lors de l’enregistrement de la commande',
            'body': e
        }

        self.update_error_response = lambda id, e: {
            'id': id,
            'status': 'danger',
            'header': 'Erreur lors de la modification de la commande',
            'body': e
        }

        self.p1 = Product.objects.create(name='product1', weight=1,
                                         price=10, display=True)
        self.p2 = Product.objects.create(name='prduct2', weight=2,
                                         price=20, display=True, step=0.25)
        self.p3 = Product.objects.create(name='product3', weight=3,
                                         price=30, display=False)

        self.command = Command.objects.create(user=self.super_user)
        Amount.objects.create(command=self.command, product=self.p1, amount=10)

        self.client = APIClient()
        self.client.login(username='test1', password='password')

    def test_list_command(self):
        """ For test if list command display good value. """

        response = self.client.get('/api/citrus/command')
        content = response.data[0]
        self.assertJSONEqual(str(response.content, encoding='utf8'), [
            {
                'user': {
                    'id': content['user']['id'],
                    'username': 'test1',
                    'email': 'test1@test.com',
                    'last_name': '',
                    'first_name': '',
                },
                'amounts': [{
                    'id': content['amounts'][0]['id'],
                    "product":
                        {
                            'id': content['amounts'][0]['product']['id'],
                            'name': 'product1',
                            'weight': float(1),
                            'description': '',
                            'step': float(1),
                            'maximum': 100,
                            'price': float(10),
                            'total': float(10),
                            'display': True,
                            'maybe_not_available': False
                    },
                    "amount": float(10)
                }],
                'total': self.command.get_total(),
                'id': content['id'],
            }
        ])
        self.assertEqual(response.status_code, 200)

    def test_add_command(self):
        """ For test add_command system with good datas. """

        data = {
            'user': 2,
            'send_mail': 1,
            'amounts': {self.p1.id: 3,
                        self.p2.id: 2}
        }

        response = self.client.post(
            reverse('command-list'), data, format='json')
        self.assertEqual(response.data, {
            'id': int(response.data['id']),
            'status': 'success',
            'header': 'Commande enregistrée',
            'body': 'Votre commande a bien été enregistrée.'
        })
        self.assertEqual(response.status_code, 200)

        Command.objects.get(user_id=2).delete()

    def test_case_number_add_command(self):
        """ For test if case number is too large (the limits is 6) and this is apply only in product with weight != 1 so on p2 here."""

        data = {
            'user': self.user.id,
            'send_mail': '1',
            'amounts': {self.p1.id: 10,
                        self.p2.id: 7}
        }

        response = self.client.post(
            reverse('command-list'), data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'id': response.data['id'],
            'status': 'danger',
            'header': 'Erreur lors de l’enregistrement de la commande',
            'body': 'Le nombre de caisse est limité à 6, vous avez commandé 7.0 caisses. Merci de modifier la commande.'
        })

    def test_bad_product_add_command(self):
        """ For test if user send bad data of product an unavailable product for example."""

        data = {
            'user': self.user.id,
            'send_mail': '1',
            'amounts': {self.p1.id: 1,
                        self.p3.id: 4}
        }

        response = self.client.post(
            reverse('command-list'), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), self.add_error_response(
            response.data['id'], 'Une erreur est survenue, merci de réessayer. (ERREUR: Product matching query does not exist.)'))

    def test_bad_user_add_command(self):
        """ Test if user send bad user_id (random number for example). """

        data = {
            'user': int(random() * 100000),
            'send_mail': '1',
            'amounts': {self.p1.id: 3,
                        self.p2.id: 4}
        }

        response = self.client.post(
            reverse('command-list'), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), self.add_error_response(
            response.data['id'], 'User matching query does not exist.'))

    def test_bad_key_add_command(self):
        """ Test if user send bad key. """

        data = {
            'wrong_data': self.user.id,
            'amounts': {self.p1.id: 3}
        }

        response = self.client.post(
            reverse('command-list'), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), self.add_error_response(
            response.data['id'], "'user'"))

    def test_bad_data_add_command(self):
        """ Test if user send bad Value of key. """
        data = {
            'user': 'wrong_id',
            'send_mail': 'true',
            'amounts': {self.p1.id: 'wrong_amount',
                        self.p2.id: 4}
        }

        response = self.client.post(
            reverse('command-list'), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), self.add_error_response(
            response.data['id'], "invalid literal for int() with base 10: 'wrong_id'"))

    def test_bad_amount_add_command(self):
        """ Test if user send bad amount for a product.
        This critere is define with step attriut. """
        data = {
            'user': self.user.id,
            'send_mail': '1',
            'amounts': {self.p2.id: 1.70}
        }

        response = self.client.post(
            reverse('command-list'), data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), self.add_error_response(
            response.data['id'], 'Une erreur est survenue, merci de réessayer. (ERREUR: )'))

    def test_also_command(self):
        """ Test if user as also command. """
        data = {
            'user': self.user.id,
            'send_mail': '1',
            'amounts': {self.p1.id: 4,
                        self.p2.id: 3}
        }

        #self.client.post(reverse('command-list'), data)
        response = self.client.post(
            reverse('command-list'), data, format='json')

        data = {
            'user': self.user.id,
            'send_mail': '1',
            'amounts': {self.p1.id: 4,
                        self.p2.id: 3}
        }

        #self.client.post(reverse('command-list'), data)
        response = self.client.post(
            reverse('command-list'), data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'id': int(response.data['id']),
            'status': 'warning',
            'header': 'Vous avez déjà commandé !',
            'body': 'Une commande à votre nom a déjà été trouvé ! '
            'Merci de vérifier que votre commande n\'est pas déjà '
            'présente dans le tableau. Si cette commande n\'est pas de vous, '
            'merci de me contacter.'
        })

    def test_update_command(self):
        """ Test if user send good data."""
        data = {
            'user': self.super_user.id,
            'amounts': {self.p1.id: 10,
                        self.p2.id: 1.25}
        }

        response = self.client.put(
            reverse('command-detail', kwargs={'pk': self.command.id}), data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'id': response.data['id'],
            'status': 'success',
            'header': 'Commande modifiée',
            'body': 'La commande de {} a bien été modifiée.'.format(self.super_user.username)
        })

    def test_number_case_update_command(self):
        """ Like add_command."""
        data = {
            'user': self.super_user.id,
            'amounts': {self.p2.id: 7}
        }

        response = self.client.put(
            reverse('command-detail', kwargs={'pk': self.command.id}), data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'id': response.data['id'],
            'status': 'danger',
            'header': 'Erreur lors de la modification de la commande',
            'body': 'Le nombre de caisse est limité à 6, vous avez commandé 7.0 caisses. Merci de modifier la commande.'
        })

    def test_bad_product_update_command(self):
        """ Like add_command."""
        data = {
            'user': self.super_user.id,
            'amounts': {self.p1.id: 1,
                        self.p3.id: 4}
        }

        response = self.client.put(
            reverse('command-detail', kwargs={'pk': self.command.id}), data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), self.update_error_response(
            response.data['id'], 'Une erreur est survenue, merci de réessayer. (ERREUR: Product matching query does not exist.)'))

    def test_bad_data_update_command(self):
        """ Like add_command."""
        data = {
            'user': 'wrong_id',
            'amounts': {self.p1.id: 'wrong_amount',
                        self.p2.id: 4}
        }

        response = self.client.put(
            reverse('command-detail', kwargs={'pk': self.command.id}), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), self.update_error_response(
            response.data['id'], "invalid literal for int() with base 10: 'wrong_id'"))

    def test_bad_amount_update_command(self):
        """ Like add_command."""
        data = {
            'user': self.super_user.id,
            'amounts': {self.p2.id: 1.70}
        }

        response = self.client.put(
            reverse('command-detail', kwargs={'pk': self.command.id}), data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), self.update_error_response(
            response.data['id'], 'Une erreur est survenue, merci de réessayer. (ERREUR: )'))


class CoffeeApiTestCase (CommandApiTestCase):
    """ This classe test all Api of coffee."""

    def setUp(self):
        super().setUp()
        OriginCoffee.objects.create(name='Origin 1')
        OriginCoffee.objects.create(name='Origin 2')
        OriginCoffee.objects.create(name='Origin 3')

        self.type1 = TypeCoffee.objects.create(name='Type 1')
        self.type2 = TypeCoffee.objects.create(name='Type 2')
        self.type3 = TypeCoffee.objects.create(name='Type 3')

        self.error_response = lambda id, e, action: {
            'id': id,
            'status': 'danger',
            'header': 'Erreur lors de {action} de la commande de café'.format(action=action),
            'body': str(e)
        }

        self.coffee1 = Coffee.objects.create(origin=OriginCoffee.objects.get(name='Origin 1'), farm_coop='coffee 1', region='region_coffee 1', process='process_coffee 1',
                                             variety='variety_coffee 1', two_hundred_gram_price=5, kilogram_price=20)
        self.coffee1.available_type.set(TypeCoffee.objects.all())
        self.coffee2 = Coffee.objects.create(origin=OriginCoffee.objects.get(name='Origin 2'), farm_coop='coffee 2', region='region_coffee 2',
                                             process='process_coffee 2', two_hundred_gram_price=7, kilogram_price=21)
        self.coffee2.available_type.set(TypeCoffee.objects.all()[:2])
        self.coffee3 = Coffee.objects.create(origin=OriginCoffee.objects.get(name='Origin 3'), farm_coop='coffee 3',
                                             region='region_coffee 3', process='process_coffee 3',  display=False)
        self.coffee3.available_type.set(TypeCoffee.objects.all())

        self.command = CommandCoffee.objects.create(
            name='name 1', first_name='first_name 2', email='command1@command1.com', phone_number='0611111111')
        self.command.coffee.add(self.coffee1, through_defaults={
            'quantity': 3,
            'weight': 200,
            'sort': self.type1
        })

        self.client = APIClient()
        self.client.login(username='test1', password='password')

    def test_create_command(self):
        data = {
            'name': 'name 1',
            'first_name': 'first_name 1',
            'email': 'email1@test.com',
            'phone_number': '0600000000',
            'command': [
                {
                    'id_coffee': self.coffee1.id,
                    'sort': self.type1.id,
                    'weight': 200,
                    'quantity': 1
                },
                {
                    'id_coffee': self.coffee2.id,
                    'sort': self.type2.id,
                    'weight': 1000,
                    'quantity': 2
                }
            ]
        }

        response = self.client.post(
            reverse('coffee-command-coffee-list'), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'id': int(response.data['id']),
            'status': 'success',
            'header': 'Commande enregistrée !',
            'body': 'Votre commande a bien été enregistrée, merci d’envoyer un mail à l’adresse da-max@tutanota.com si vous souhaitez la modifier.'
        })

    def test_bad_email_create_command(self):
        data = {
            'name': 'name 1',
            'first_name': 'first_name 1',
            'email': 'email.com',
            'phone_number': '0600000000',
            'command': [
                {
                    'id_coffee': self.coffee1.id,
                    'sort': self.type1.id,
                    'weight': 200,
                    'quantity': 2
                },
                {
                    'id_coffee': self.coffee2.id,
                    'sort': self.type2.id,
                    'weight': 1000,
                    'quantity': 3
                }
            ]
        }

        response = self.client.post(
            reverse('coffee-command-coffee-list'), data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'id': int(response.data['id']),
            'status': 'danger',
            'header': 'Erreur lors de l’enregistrement de la commande de café',
            'body': 'L’email rentré ou le numéro de télephone n’est pas valide, merci de vérifier qu’ils sont corrects et de réessayer. (ERREUR : )'
        })

    def test_bad_phone_number_create_command(self):
        data = {
            'name': 'name 1',
            'first_name': 'first_name 1',
            'email': 'email@email.com',
            'phone_number': 'azertyuiop',
            'command': [
                {
                    'id_coffee': self.coffee1.id,
                    'sort': self.type1.id,
                    'weight': 200,
                    'quantity': 2
                },
                {
                    'id_coffee': self.coffee2.id,
                    'sort': self.type2.id,
                    'weight': 1000,
                    'quantity': 3
                }
            ]
        }

        response = self.client.post(
            reverse('coffee-command-coffee-list'), data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'id': int(response.data['id']),
            'status': 'danger',
            'header': 'Erreur lors de l’enregistrement de la commande de café',
            'body': 'L’email rentré ou le numéro de télephone n’est pas valide, merci de vérifier qu’ils sont corrects et de réessayer. (ERREUR : )'
        })

    def test_bad_coffee_create_command(self):
        data = {
            'name': 'name 1',
            'first_name': 'first_name 1',
            'email': 'email@email.com',
            'phone_number': '0600000000',
            'command': [
                {
                    'id_coffee': int(random() * 10000),
                    'sort': self.type1.id,
                    'weight': 200,
                    'quantity': 2
                },
                {
                    'id_coffee': self.coffee2.id,
                    'sort': self.type2.id,
                    'weight': 1000,
                    'quantity': 3
                }
            ]
        }

        response = self.client.post(
            reverse('coffee-command-coffee-list'), data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'id': int(response.data['id']),
            'status': 'danger',
            'header': 'Erreur lors de l’enregistrement de la commande de café',
            'body': 'Un ou plusieurs café commandé n’existe pas, merci de vérifier la commande et de réessayer. (ERREUR : Coffee matching query does not exist.)'
        })

    def test_bad_sort_create_command(self):
        data = {
            'name': 'name 1',
            'first_name': 'first_name 1',
            'email': 'email@email.com',
            'phone_number': '0600000000',
            'command': [
                {
                    'id_coffee': self.coffee1.id,
                    'sort': self.type1.id,
                    'weight': 200,
                    'quantity': 2
                },
                {
                    'id_coffee': self.coffee2.id,
                    'sort': self.type3.id,
                    'weight': 1000,
                    'quantity': 3
                }
            ]
        }

        response = self.client.post(
            reverse('coffee-command-coffee-list'), data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'id': int(response.data['id']),
            'status': 'danger',
            'header': 'Erreur lors de l’enregistrement de la commande de café',
            'body': 'Un ou plusieurs café commandé n’existe pas, merci de vérifier la commande et de réessayer. (ERREUR : Type matching query does not exist.)'
        })

    def test_bad_weight_create_command(self):
        data = {
            'name': 'name 1',
            'first_name': 'first_name 1',
            'email': 'email@email.com',
            'phone_number': '0600000000',
            'command': [
                {
                    'id_coffee': self.coffee1.id,
                    'sort': self.type1.id,
                    'weight': 2000,
                    'quantity': 2
                },
                {
                    'id_coffee': self.coffee2.id,
                    'sort': self.type2.id,
                    'weight': 1000,
                    'quantity': 3
                }
            ]
        }

        response = self.client.post(
            reverse('coffee-command-coffee-list'), data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'id': int(response.data['id']),
            'status': 'danger',
            'header': 'Erreur lors de l’enregistrement de la commande de café',
            'body': 'La quantité ou le poids commandé n’est pas valide, merci de vérifier la commande et de réessayer. (ERREUR : )'
        })

    def test_bad_amount_create_command(self):
        data = {
            'name': 'name 1',
            'first_name': 'first_name 1',
            'email': 'email@email.com',
            'phone_number': '0600000000',
            'command': [
                {
                    'id_coffee': self.coffee1.id,
                    'sort': self.type1.id,
                    'weight': 200,
                    'quantity': 2
                },
                {
                    'id_coffee': self.coffee2.id,
                    'sort': self.type2.id,
                    'weight': 1000,
                    'quantity': 3.12
                }
            ]
        }

        response = self.client.post(
            reverse('coffee-command-coffee-list'), data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'id': int(response.data['id']),
            'status': 'danger',
            'header': 'Erreur lors de l’enregistrement de la commande de café',
            'body': 'La quantité ou le poids commandé n’est pas valide, merci de vérifier la commande et de réessayer. (ERREUR : )'
        })

    def test_not_amount_create_command(self):
        """ Test if user send request without quantity. """
        data = {
            'name': 'name 1',
            'first_name': 'first_name 1',
            'email': 'email@email.com',
            'phone_number': '0600000000',
            'command': [
                {
                    'id_coffee': self.coffee1.id,
                    'sort': self.type1.id,
                    'weight': 200,
                    'quantity': 2
                },
                {
                    'id_coffee': self.coffee2.id,
                    'sort': self.type2.id,
                    'weight': 1000,
                }
            ]
        }

        response = self.client.post(
            reverse('coffee-command-coffee-list'), data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'id': int(response.data['id']),
            'status': 'danger',
            'header': 'Erreur lors de l’enregistrement de la commande de café',
            'body': "('Erreur', KeyError('quantity',))"
        })

    def test_not_name_create_command(self):
        """ Test if user send request without name. """
        data = {
            'first_name': 'first_name 1',
            'email': 'email@email.com',
            'phone_number': '0600000000',
            'command': [
                {
                    'id_coffee': self.coffee1.id,
                    'sort': self.type1.id,
                    'weight': 200,
                    'quantity': 2
                },
                {
                    'id_coffee': self.coffee2.id,
                    'sort': self.type2.id,
                    'weight': 1000,
                    'quantity': 3
                }
            ]
        }

        response = self.client.post(
            reverse('coffee-command-coffee-list'), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'id': int(response.data['id']),
            'status': 'danger',
            'header': 'Erreur lors de l’enregistrement de la commande de café',
            'body': '"Les champs nom, prénom, email ou numéro de télephone n’ont pas été rentrés, merci de vérifier qu’ils sont correctement renseignés, puis réessayer. (ERREUR : \'name\')"'
        })

    def test_not_id_coffee_create_command(self):
        """ Test if an user try to command without id_coffee. """
        data = {
            'first_name': 'first_name 1',
            'email': 'email@email.com',
            'phone_number': '0600000000',
            'name': 'name 1',
            'command': [
                {
                    'sort': self.type1.id,
                    'weight': 200,
                    'quantity': 2
                },
                {
                    'id_coffee': self.coffee2.id,
                    'sort': self.type2.id,
                    'weight': 1000,
                    'quantity': 3
                }
            ]
        }

        response = self.client.post(
            reverse('coffee-command-coffee-list'), data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'id': int(response.data['id']),
            'status': 'danger',
            'header': 'Erreur lors de l’enregistrement de la commande de café',
            'body': "('Erreur', KeyError('id_coffee',))"
        })

    def test_bad_pk_update_command(self):
        """ Test if user send request with bad pk. """
        data = {
            'name': 'name 1',
            'first_name': 'first_name 1',
            'email': 'email1@test.com',
            'phone_number': '0600000000',
            'command': [
                {
                    'id_coffee': self.coffee1.id,
                    'sort': self.type1.id,
                    'weight': 200,
                    'quantity': 1
                },
                {
                    'id_coffee': self.coffee2.id,
                    'sort': self.type2.id,
                    'weight': 1000,
                    'quantity': 2
                }
            ]
        }

        response = self.client.put(reverse(
            'coffee-command-coffee-detail', kwargs={'pk': int(random() * 10000)}), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), self.error_response(
            response.data['id'], 'CommandCoffee matching query does not exist.', 'la modification'))

    def test_delete_command(self):
        """ Test if user want delete CoffeeCommand. """

        response = self.client.delete(
            reverse('coffee-command-coffee-detail', kwargs={'pk': self.command.id}))

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'id': int(response.data['id']),
            'status': 'success',
            'header': 'Commande supprimée',
            'body': 'La commande de {} {} a bien été supprimée.'.format(self.command.first_name, self.command.name)
        })

    def test_bad_pk_delete_command(self):
        """ Test if an user want delete CoffeeCommand with bad pk. """

        response = self.client.delete(
            reverse('coffee-command-coffee-detail', kwargs={'pk': int(random() * 1000)}))

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), self.error_response(
            response.data['id'], 'CommandCoffee matching query does not exist.', 'la suppression'))
