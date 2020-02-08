from django.test import TestCase

from django.contrib.auth.models import User

from command.models import Amount, Command, Product

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