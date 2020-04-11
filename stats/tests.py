from django.test import TestCase, Client, TransactionTestCase
from django.utils import timezone
from django.urls import reverse

from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in

from stats.models import PageAccess
from registration.views import connect


class CheckAccessTest(TransactionTestCase):
    """ Class for test middleware CheckAccess. """

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_superuser(
            'test1', 'test1@test.com', 'password')
        user_logged_in.disconnect(receiver=connect)

        self.client = Client()
        self.client.login(username='test1', password='password')

    def test_page_not_define(self):
        PageAccess.objects.create(name='Page', url='http://testserver/', access=True,
                                  raise_exception=True, title='Warning', content='Warning', start_date=timezone.now())
        response = self.client.get(reverse('list_article'))

        self.assertEqual(response.status_code, 200)

    def test_access_true(self):
        PageAccess.objects.create(name='Page', url='http://testserver/', access=True,
                                  raise_exception=True, title='Warning', content='Warning', start_date=timezone.now())
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_access_false(self):
        PageAccess.objects.create(name='Page', url='http://testserver/', access=False,
                                  raise_exception=True, title='Warning', content='Warning', start_date=timezone.now())
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 404)
    
    def test_raise_excption_false(self):
        PageAccess.objects.create(name='Page', url='http://testserver/', access=False,
                                  raise_exception=False, title='Warning', content='Warning', start_date=timezone.now())
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)