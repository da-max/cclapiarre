from django.test import TestCase, TransactionTestCase, Client
from django.template.loader import render_to_string
from django.urls import reverse


from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in

from backend.citrus.models import Amount, Command, Product
from backend.registration.views import connect



class AmountTestCase(TestCase):
    
    def setUp(self):
        product1 = Product.objects.create(
            name="Orange", 
            description="Test1", 
            weight=12,
            price=19.45,
            display=True
        )

        product2 = Product.objects.create(
            name="Clémentine",
            description="Test2",
            weight=1,
            price=30,
            display=True
        )

        user1 = User.objects.create(
            username="exemple",
            password="1",
            email="test@test.com"
        )

        user2 = User.objects.create(
            username="exemple2",
            password="2",
            email="test2@test.com"
        )

        command1 = Command.objects.create(
            number=1,
            user=user1
        )

        command2 = Command.objects.create(
            number=2,
            user=user2
        )

        Amount.objects.create(product=product1, command=command1, amount=12)
        Amount.objects.create(product=product2, command=command1, amount=4)
        Amount.objects.create(product=product1, command=command2, amount=24)
    
    
    def test_get_total_product(self):

        product = Product.objects.get(name="Orange")
        total = Amount.get_total_product(Amount, product=product)
        self.assertEqual(total, 36)
    
    
    def test_get_total_user(self):

        command = Command.objects.get(number=1)
        total = Amount.get_total_user(Amount, command)
        self.assertEqual(total, 353.4)



class ViewTest(TransactionTestCase):
    """ ViewTest is class for test all view of command apps."""
    
    
    def setUp(self):
        user_logged_in.disconnect(receiver=connect)
        
        user = User.objects.create_superuser('test1', 'test1@test.com', 'password')
        
        self.client = Client()
        self.client.login(username='test1', password='password')
    
    
    def test_command_citrus(self):
        """ Test if command_citrus display app.html template (vuejs app)."""
        
        response = self.client.get(reverse('citrus:new_command_citrus'))
        
        self.assertEqual(response.status_code, 200)
        with self.assertTemplateUsed('app.html'):
            render_to_string('app.html')
    
    
    def test_sommary_command(self):
        """ Test if sommary_command display command/pdf/sommary_command template. """
        
        response = self.client.get(reverse('citrus:sommary_command'))
        
        self.assertEqual(response.status_code, 200)
        with self.assertTemplateUsed('citrus/pdf/sommary_command.html'):
            render_to_string('citrus/pdf/sommary_command.html')