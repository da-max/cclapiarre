from django.test import TestCase, TransactionTestCase, Client
from django.db.models import Q
from django.template.loader import render_to_string


from django.contrib.auth.models import User, Permission
from django.contrib.auth.signals import user_logged_in
from django.contrib.contenttypes.models import ContentType


from backend.coffee.models import CoffeeOrder, Coffee, Origin, Type, CoffeeAmount


class ViewTest(TransactionTestCase):
    """ ViewTest is classe for test all view of coffee apps. """

    def setUp(self):

        origin1 = Origin.objects.create(name="origin1")
        type1 = Type.objects.create(name='type1')
        type2 = Type.objects.create(name='type2')

        types = Type.objects.all()

        coffee1 = Coffee.objects.create(origin=origin1, farm_coop="coffee1", region="region1",
                                        description="description1", process="process1", variety="variety1",
                                        two_hundred_gram_price=5, kilogram_price=20,
                                        display=True, maximum=100)

        coffee1.available_type.set(Type.objects.all())

        self.user = User.objects.create_superuser(
            'test1', 'test1@test.com', 'password')
        self.client = Client()
        self.client.login(username='test1', password='password')

    def test_list_coffee(self):
        """ Test list coffee template, so this class
        test all coffee pages for make sure it exits, and good value is displayed. """
        response = self.client.get('/cafe/liste-des-cafes')

        self.assertEqual(response.status_code, 200)
        # Test if template content contains title (h1) of page.
        self.assertTemplateUsed(response, 'coffee/coffee/list.html')

    def test_create_coffee(self):
        """ Test coffee/coffee/new.html template."""

        response = self.client.get('/cafe/creer-un-cafe')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'coffee/coffee/new.html')

    def test_update_coffee(self):
        """ Test coffee/coffee/update template. """

        coffee = Coffee.objects.get(farm_coop='coffee1')
        response = self.client.get('/cafe/modifier-un-cafe/' + str(coffee.id))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'coffee/coffee/update.html')

    def test_global_command(self):
        """ Test coffee/command/global_command template."""

        response = self.client.get('/cafe/commande-globale')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'coffee/command/global_command.html')

    def test_list_origin(self):
        """ Test /coffee/origin/list.html template. """

        response = self.client.get('/cafe/liste-des-origines')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'coffee/origin/list.html')

    def test_create_origin(self):
        """ Test /coffee/origin/new.html. """

        response = self.client.get('/cafe/creer-une-origine')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'coffee/origin/new.html')

    def test_update_origin(self):
        """ Test /coffee/origin/update.html template."""

        origin = Origin.objects.get(name='origin1')
        response = self.client.get(
            '/cafe/modifier-une-origine/' + str(origin.id))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'coffee/origin/update.html')

    def test_pdf_global_command(self):
        """ Test /coffee/pdf/global_command.html template. """

        response = self.client.get('/cafe/pdf-commande-globale')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'coffee/pdf/global_command.html')


class PermissionsCoffeeTest(TestCase):
    """ PermissionsCoffeeTest is class for test all permissions of coffee apps."""

    def setUp(self):

        self.content_type = ContentType.objects.filter(app_label='coffee')
        self.user = User.objects.create_user(
            'permission_coffee', 'test@test.com', 'password')
        self.origin = Origin.objects.create(name="origin1")
        type1 = Type.objects.create(name='type1')

        types = Type.objects.all()

        self.coffee = Coffee.objects.create(origin=self.origin, farm_coop="coffee1", region="region1",
                                            description="description1", process="process1", variety="variety1",
                                            two_hundred_gram_price=5, kilogram_price=20,
                                            display=True, maximum=100)

        self.coffee.available_type.set(Type.objects.all())

        self.command_coffee = CoffeeOrder.objects.create(
            name='Test', first_name='First test', email='test@test.com', phone_number='0659617169')

        self.client = Client()
        self.client.login(username='permission_coffee', password='password')

    def test_list_coffee(self):
        """ Test if user has good permission for access to ListCoffee view."""

        permission = Permission.objects.get(Q(codename='view_coffee') & Q(
            content_type=self.content_type.get(model='coffee')))
        self.user.user_permissions.set([permission])

        response = self.client.get('/cafe/liste-des-cafe')

        self.assertEqual(response.status_code, 200)

    def test_bad_list_coffee(self):
        """ Test if user has not permission for access to ListCoffee."""

        response = self.client.get('/cafe/liste-des-cafes')

        self.assertEqual(response.status_code, 403)

    def test_create_coffee(self):
        """ Test if user has add_coffee for acess to CreateCoffee view."""

        permission = Permission.objects.get(Q(codename='add_coffee') & Q(
            content_type=self.content_type.get(model='coffee')))
        self.user.user_permissions.set([permission])

        response = self.client.get('/cafe/creer-un-cafe')

        self.assertEqual(response.status_code, 200)

    def test_bad_create_coffee(self):
        """ Test if user has not permission for access to CreateCofffee view."""

        response = self.client.get('/cafe/creer-un-cafe')

        self.assertEqual(response.status_code, 403)

    def test_update_coffee(self):
        """ Test if user has change_coffee permission for access to UpdateCoffee view."""

        permission = Permission.objects.get(Q(codename='change_coffee') & Q(
            content_type=self.content_type.get(model='coffee')))
        self.user.user_permissions.set([permission])

        response = self.client.get(
            '/cafe/modifier-un-cafe/' + str(self.coffee.id))

        self.assertEqual(response.status_code, 200)

    def test_bad_update_coffee(self):
        """ Test if user has not change_coffee permuission for access to UpdateCoffee view."""

        response = self.client.get(
            '/cafe/modifier-un-cafe/' + str(self.coffee.id))

        self.assertEqual(response.status_code, 403)

    def test_list_origin(self):
        """ Test if user has view_origin permission for access to ListOrigin."""

        permission = Permission.objects.get(Q(codename='view_origin') & Q(
            content_type=self.content_type.get(model='origin')))
        self.user.user_permissions.set([permission])

        response = self.client.get('/cafe/liste-des-origines')

        self.assertEqual(response.status_code, 200)

    def test_bad_list_origin(self):
        """ Test if user has not permission for access to ListOrigin view."""

        response = self.client.get('/cafe/liste-des-origines')

        self.assertEqual(response.status_code, 403)

    def test_create_origin(self):
        """ Test if user has add_origin for access to CreateOrigin view."""

        permission = Permission.objects.get(Q(codename='add_origin') & Q(
            content_type=self.content_type.get(model='origin')))
        self.user.user_permissions.set([permission])

        response = self.client.get('/cafe/creer-une-origine')

        self.assertEqual(response.status_code, 200)

    def test_bad_create_origin(self):
        """ Test if user has not permission for access to CreateOrigin view."""

        response = self.client.get('/cafe/creer-une-origine')

        self.assertEqual(response.status_code, 403)

    def test_update_origin(self):
        """ Test if user has change_origin for access to UpdateOrigin view."""

        permission = Permission.objects.get(Q(codename='change_origin') & Q(
            content_type=self.content_type.get(model='origin')))
        self.user.user_permissions.set([permission])

        response = self.client.get(
            '/cafe/modifier-une-origine/' + str(self.origin.id))

        self.assertEqual(response.status_code, 200)

    def test_bad_update_origin(self):
        """ Test if user has not permission for access to UpdateOrigin view."""

        response = self.client.get(
            '/cafe/modifier-une-origine/' + str(self.origin.id))

        self.assertEqual(response.status_code, 403)

    def test_delete_origin(self):
        """ Test if user has delete_origin for access to delete_origin view. """

        permission = Permission.objects.get(Q(codename='delete_origin') & Q(
            content_type=self.content_type.get(model='origin')))
        self.user.user_permissions.set([permission])

        response = self.client.get(
            '/cafe/supprimer-une-origine/' + str(self.origin.id))

        self.assertEqual(response.status_code, 302)

    def test_bad_delete_origin(self):
        """ Test if user has not permission for aceess to delete_origin view."""

        response = self.client.get(
            '/cafe/supprimer-une-origine/' + str(self.origin.id))

        self.assertEqual(response.status_code, 403)

    def test_list_command(self):
        """ Test if user has view_CoffeeOrder for access to pdf_list_command view."""
        permission = Permission.objects.get(Q(codename='view_CoffeeOrder') & Q(
            content_type=self.content_type.get(model='CoffeeOrder')))
        self.user.user_permissions.set([permission])

        response1 = self.client.get('/cafe/pdf-liste-des-commandes')
        response2 = self.client.get('/cafe/commande-globale')
        response3 = self.client.get('/cafe/pdf-commande-globale')

        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response3.status_code, 200)

    def test_bad_list_command(self):
        """ Test if user has not permission for access to pdf_list_command. """

        response1 = self.client.get('/cafe/pdf-liste-des-commandes')
        response2 = self.client.get('/cafe/commande-globale')
        response3 = self.client.get('/cafe/pdf-commande-globale')

        self.assertEqual(response1.status_code, 403)
        self.assertEqual(response2.status_code, 403)
        self.assertEqual(response3.status_code, 403)
