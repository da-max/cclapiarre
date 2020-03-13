import json
from random import random
from django.urls import reverse, path, include
from django.db.models import ObjectDoesNotExist

from rest_framework.test import APITransactionTestCase, URLPatternsTestCase, APIClient
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import User

from command.models import Amount, Product, Command
from registration.views import connect


class CitrusApiTestCase (APITransactionTestCase, URLPatternsTestCase):
    """ This class user APITransactioTestCase and URLPatternsTestCase for use urlpatterns attribut
    So this class depends to rest_framework module.
    The client is define in setUp method, this client is APIClient."""

    urlpatterns = [
        path('api/', include('api.urls')),
    ]

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
        self.super_user = User.objects.create_superuser(
            'test1', 'test1@test.com', 'password')
        self.user = User.objects.create(
            username='user1', email='user1@user.com', password='password')

        self.add_error_response = lambda id, e: {
            'id': id,
            'status': 'danger',
            'header': 'Erreur lors de l\'enregistrement des produits de votre commande',
            'body': 'Une erreur est survenue lors de l\'enregistrement d\'un (ou plusieurs) produit⋅s, \
                merci de réessayer et de me contacter si vous rencontrez de nouveau cette erreur. \
                (ERREUR : {})'.format(type(e))
        }

        self.update_error_response = lambda id, e: {
            'id': id,
            'status': 'danger',
            'header': 'Erreur lors de la modification de la commande',
            'body': 'Une erreur est survenue lors de la modification de la commande'
            'merci de réessayer et de me contacter si vous rencontrez de nouveau cette erreur. '
            '(ERREUR : {})'.format(type(e))
        }

        self.p1 = Product.objects.create(name='product1', weight=1,
                                         price=10, display=True)
        self.p2 = Product.objects.create(name='prduct2', weight=2,
                                         price=20, display=True, step=0.25)
        self.p3 = Product.objects.create(name='product3', weight=3,
                                         price=30, display=False)

        self.command = Command.objects.create(user=self.super_user)
        Amount.objects.create(command=self.command, product=self.p1, amount=10)

        user_logged_in.disconnect(receiver=connect)

        self.client = APIClient()
        self.client.login(username='test1', password='password')

    def test_list_product(self):
        """ For test if list of product display goof value. """

        response = self.client.get(reverse('product-list'))

        self.assertNotIn({
            'id': 3,
            'name': 'product3',
            'weight': float(3),
            'description': '',
            'step': float(1),
            'maximum': 100,
            'price': float(30),
            'total': float(0)
        }, response.data)
        self.assertEqual(response.status_code, 200)

    def test_list_command(self):
        """ For test if list command display good value. """

        response = self.client.get(reverse('command-list'))
        content = json.loads(response.content)[0]

        self.assertJSONEqual(response.content, [
            {
                'user': {
                    'id': content['user']['id'],
                    'username': 'test1',
                    'email': 'test1@test.com',
                    'last_name': '',
                    'first_name': '',
                },
                'product': [{
                    'id': content['product'][0]['id'],
                    'name': 'product1',
                    'weight': float(1),
                    'description': '',
                    'step': float(1),
                    'maximum': 100,
                    'price': float(10),
                    'total': float(10),
                }],
                'total': self.command.get_total(),
                'id': content['id'],
            }
        ])
        self.assertEqual(response.status_code, 200)

    def test_list_amount(self):
        """ For test if list_amount display good value. """

        response = self.client.get(reverse('amount-list'))
        content = json.loads(response.content)[0]

        self.assertJSONEqual(response.content, [
            {
                'id': content['id'],
                'command': {
                    'id': content['command']['id'],
                    'user': {
                        'id': content['command']['user']['id'],
                        'username': 'test1',
                        'email': 'test1@test.com',
                        'last_name': '',
                        'first_name': ''
                    }
                },
                'product': {
                    'id': content['product']['id'],
                    'name': 'product1',
                    'weight': float(1),
                    'description': '',
                    'step': float(1),
                    'maximum': 100,
                    'price': float(10),
                    'total': float(10)
                },
                'amount': float(10)
            }
        ])
        self.assertEqual(response.status_code, 200)

    def test_add_command(self):
        """ For test add_command system with good datas. """

        data = {
            'user': 2,
            'send_mail': 'true',
            self.p1.id: 3,
            self.p2.id: 2,
        }

        response = self.client.post(reverse('command-list'), data)

        self.assertJSONEqual(response.content, {
            'id': float(json.loads(response.content)['id']),
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
            'send_mail': 'true',
            self.p1.id: 10,
            self.p2.id: 7
        }

        response = self.client.post(reverse('command-list'), data)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            'id': json.loads(response.content)['id'],
            'status': 'warning',
            'header': 'Nombre de caisse trop important',
            'body': 'Le nombre de caisse que vous avez commandé est trop important. '
            'Le nombre maximum de caisse est fixé à 6 par adhérent. Merci de modifier votre commande.'
        })

    def test_bad_product_add_command(self):
        """ For test if user send bad data of product an unavailable product for example."""

        data = {
            'user': self.user.id,
            'send_mail': 'true',
            self.p1.id: 1,
            self.p3.id: 4
        }

        response = self.client.post(reverse('command-list'), data)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.add_error_response(
            json.loads(response.content)['id'], Product.DoesNotExist()))

    def test_bad_user_add_command(self):
        """ Test if user send bad user_id (random number for example). """

        data = {
            'user': int(random() * 100000),
            'send_mail': 'true',
            self.p1.id: 3,
            self.p2.id: 4
        }

        response = self.client.post(reverse('command-list'), data)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.add_error_response(
            json.loads(response.content)['id'], User.DoesNotExist()))

    def test_bad_key_add_command(self):
        """ Test if user send bad key. """

        data = {
            'wrong_data': self.user.id,
            self.p1.id: 3
        }

        response = self.client.post(reverse('command-list'), data)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.add_error_response(
            json.loads(response.content)['id'], KeyError()))

    def test_bad_data_add_command(self):
        """ Test if user send bad Value of key. """
        data = {
            'user': 'wrong_id',
            'send_mail': 'true',
            self.p1.id: 'wrong_amount',
            self.p2.id: 4
        }

        response = self.client.post(reverse('command-list'), data)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.add_error_response(
            json.loads(response.content)['id'], ValueError()))

    def test_bad_amount_add_command(self):
        """ Test if user send bad amount for a product.
        This critere is define with step attriut. """
        data = {
            'user': self.user.id,
            'send_mail': 'true',
            self.p2.id: 1.70
        }

        response = self.client.post(
            reverse('command-list'), data)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.add_error_response(
            json.loads(response.content)['id'], AssertionError()))

    def test_also_command(self):
        """ Test if user as also command. """
        data = {
            'user': self.user.id,
            'send_mail': 'true',
            self.p1.id: 4,
            self.p2.id: 3
        }

        self.client.post(reverse('command-list'), data)
        response = self.client.post(reverse('command-list'), data)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            'id': json.loads(response.content)['id'],
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
            'user_id': self.super_user.id,
            self.p1.id: 10,
            self.p2.id: 1.25
        }

        response = self.client.put(
            reverse('command-detail', kwargs={'pk': self.command.id}), data)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            'id': json.loads(response.content)['id'],
            'status': 'success',
            'header': 'Commande modifiée',
            'body': 'La commande de {} a bien été modifié.'.format(self.super_user.username)
        })

    def test_number_case_update_command(self):
        """ Like add_command."""
        data = {
            'user_id': self.super_user.id,
            self.p2.id: 7
        }

        response = self.client.put(
            reverse('command-detail', kwargs={'pk': self.command.id}), data)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            'id': json.loads(response.content)['id'],
            'status': 'warning',
            'header': 'Nombre de caisse trop important',
            'body': 'Le nombre de caisse commandé est trop important. '
            'Le nombre maximum de caisse est fixé à 6 par adhérent. Merci de modifier la commande.'
        })

    def test_bad_product_update_command(self):
        """ Like add_command."""
        data = {
            'user_id': self.super_user.id,
            self.p1.id: 1,
            self.p3.id: 4
        }

        response = self.client.put(
            reverse('command-detail', kwargs={'pk': self.command.id}), data)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.update_error_response(
            json.loads(response.content)['id'], Product.DoesNotExist()))

    def test_bad_data_update_command(self):
        """ Like add_command."""
        data = {
            'user_id': 'wrong_id',
            self.p1.id: 'wrong_amount',
            self.p2.id: 4
        }

        response = self.client.put(
            reverse('command-detail', kwargs={'pk': self.command.id}), data)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.update_error_response(
            json.loads(response.content)['id'], ValueError()))

    def test_bad_amount_update_command(self):
        """ Like add_command."""
        data = {
            'user_id': self.super_user.id,
            self.p2.id: 1.70
        }

        response = self.client.put(
            reverse('command-detail', kwargs={'pk': self.command.id}), data)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.update_error_response(
            json.loads(response.content)['id'], AssertionError()))
