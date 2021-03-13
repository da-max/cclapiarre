from django.test import TestCase, TransactionTestCase, Client
from django.urls import reverse

from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import User

from registration.views import connect


class BaseTest(TransactionTestCase):
    """ Class for define all ViewTest."""

    def setUp(self):

        # Disconnet signal for don't send message.
        user_logged_in.disconnect(receiver=connect)
        self.client = Client()


class ViewTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_superuser(
            'test1', 'test1@test.com', 'password')
        self.client.login(username='test1', password='password')


class RegistrationViewTest(ViewTest):
    def setUp(self):
        super().setUp()

        self.user1 = User.objects.create(
            username='user 1',
            email='user1@user1.com',
            password='password1'
        )

        self.user2 = User.objects.create(
            username='user 2',
            email='user2@user2.com',
            password='password2'
        )

    def test_list_all_user(self):
        response = self.client.get(reverse('list_all_user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/user/list.html')

    def test_create_user(self):
        response = self.client.get(reverse('create_user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/user/new.html')

    def test_update_user(self):
        response = self.client.get(
            reverse('update_user', kwargs={'pk': self.user1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/user/update.html')

    def test_bad_pk_update_user(self):
        response = self.client.get(
            reverse('update_user', kwargs={'pk': int(self.user2.id) + 100}))
        self.assertEqual(response.status_code, 404)
