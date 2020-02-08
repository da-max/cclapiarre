from django.test import TestCase, Client

from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.signals import Signal

from pasta.models import *
from registration.views import connect


class NewCommandPastaTest(TestCase):


    def setUp(self):
        
        user_logged_in.disconnect(receiver=connect)
        user = User.objects.create_superuser(
            'test1', 'test1@test.com', 'password')
        category1 = Category.objects.create(name='category1')
        unit1 = Unit.objects.create(name='unit1')
        product1 = Product.objects.create(name='product1')
        metadata_product = MetadataProduct.objects.create(product=product1,
                                           weight='1',
                                           unit=unit1,
                                           price=10.53,
                                           category=category1)
        self.client = Client()
        self.client.login(username='test1', password='password')


    def test_bad_product_name(self):
        """ Test if user send bad product name """
        
        data = {
            'name': 'name1',
            'first_name': 'first_name1',
            'email': 'email1',
            'phone_number': '06000000',
            '0': 'bad_product\\1\\1'
        }
        
        response = self.client.post('/pate/create-command', data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['body'], 'Le produit bad_product n\'est pas disponible, merci d\'actualiser la page, '
            'de recommander et de me contacter si vous rencontrez de nouveau cette erreur.')
    
    
    def test_bad_weight(self):
        """ Test if user send bad weight for product. """
        
        data = {
            'name': 'name1',
            'first_name': 'first_name1',
            'email': 'email1',
            'phone_number': '06000000',
            '0': 'product1\\500\\2'
        }
        
        response = self.client.post('/pate/create-command', data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['body'], 'Le produit product1 n\'est pas disponible, merci d\'actualiser la page, '
                        'de recommander et de me contacter si vous rencontrez de nouveau cette erreur.')
    
    
    def test_bad_len_metadata(self):
        """ Test if user send bad metadata (too small or too len) """

        data = {
            'name': 'name1',
            'first_name': 'first_name1',
            'email': 'email1',
            'phone_number': '06000000',
            '0': 'product1\\2\\3\\3'
        }
        
        response = self.client.post('/pate/create-command', data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['body'], 'Une erreur est survenue, merci d\'actualiser la page, '
                        'de recommander et de me contacter si vous rencontrez de nouveau'
                        'cette erreur (code d\'erreur: p.len).')
    
    
    def test_bad_amount(self):
        """ Test if user send bad type of amount. """
        
        data = {
            'name': 'name1',
            'first_name': 'first_name1',
            'email': 'email1',
            'phone_number': '06000000',
            '0': 'product1\\1\\bad amout'
        }
        
        response = self.client.post('/pate/create-command', data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['body'], 'Votre commande n\'a pas pu être enregistrée, '
                    'merci de réesayer et de me contacter si vous '
                    'recontrez de nouveau une erreur.')
    
    
    def test_mail(self):
        """ Test if user have not send mail. """
        
        data = {
            'name': 'name1',
            'phone_number': '06000000',
            'first_name': 'first_name1',
            '0': 'product1\\1\\2'
        }
        
        response = self.client.post('/pate/create-command', data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['body'], 'Les données personnelles que vous avez rentrées ne '
                    'sont pas valides, merci de les vérifier puis réessayer.')
    
    
    def test_first_name(self):
        """ Test if user have not send first_name. """
        
        data = {
            'name': 'name1',
            'phone_number': '06000000',
            'email': 'email1',
            '0': 'product1\\1\\3'
        }
        
        response = self.client.post('/pate/create-command', data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['body'], 'Les données personnelles que vous avez rentrées ne '
                    'sont pas valides, merci de les vérifier puis réessayer.')
    
    
    def test_name(self):
        """ Test if user have not send name. """
        
        data = {
            'first_name': 'fisrt_name1',
            'email': 'email1',
            'phone_number': '06000000',
            '0': 'product1\\1\\3'
        }
        
        response = self.client.post('/pate/create-command', data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['body'], 'Les données personnelles que vous avez rentrées ne '
                    'sont pas valides, merci de les vérifier puis réessayer.')
    
    
    def test_phone_number(self):
        """ Test if user have not send phone_number. """
        
        data = {
            'first_name': 'fisrt_name1',
            'email': 'email1',
            'name': 'name1',
            '0': 'product1\\1\\3'
        }
        
        response = self.client.post('/pate/create-command', data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['body'], 'Les données personnelles que vous avez rentrées ne '
                    'sont pas valides, merci de les vérifier puis réessayer.')

    
    def test_already_command(self):
        """ Test if user have already commant. """
        
        product1 = MetadataProduct.objects.get(product__name='product1')
        
        command = CommandPasta.objects.create(name='name1', first_name='first_name1', email='email1', phone_number='06000000')
        amount = Amount.objects.create(product=product1, command=command, amount=3)
        
        data = {
            'first_name': 'fisrt_name1',
            'email': 'email1',
            'phone_number': '06000000',
            'name': 'name1',
            '0': 'product1\\1\\3'
        }
        
        response = self.client.post('/pate/create-command', data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['header'], 'Vous avez déjà commandé !')
    
    
    def test_method(self):
        """ Test if user have not send data with post method. """
        
        data = {
            'first_name': 'fisrt_name1',
            'email': 'email1',
            'phone_number': '06000000',
            'name': 'name1',
            '0': 'product1\\1\\3'
        }
        
        response = self.client.get('/pate/create-command', follow=True)
        
        self.assertEqual(response.status_code, 200)
    
    
    def test_command(self):
        """ Test if user send good data. """
        
        data = {
            'name': 'name1',
            'first_name': 'first_name1',
            'email': 'email1',
            'phone_number': '06000000',
            '0': 'product1\\1\\4'
        }
        
        response = self.client.post('/pate/create-command', data)
        
        self.assertEqual(response.status_code, 200)