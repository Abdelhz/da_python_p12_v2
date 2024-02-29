from django.core.management import call_command
from django.test import TestCase
from django.contrib.auth import get_user_model
from io import StringIO
from CustomUser.models import CustomUserAccount, Team, CustomToken
from Epic_Events.utils import refresh_or_create_token, verify_token


class UserCommandTestCase(TestCase):
    def setUp(self):
        self.out = StringIO()
        self.err = StringIO()
        self.user1 = CustomUserAccount.objects.create_user(
            username='admin',
            password='admin',
            email='admin@example.com',
            first_name='Super',
            last_name='User',
            phone_number='1234567891',
            team_name='management',
            is_superuser=True
        )
        self.user2 = CustomUserAccount.objects.create_user(
            username='manager',
            password='admin',
            email='manager@example.com',
            first_name='Manager',
            last_name='User',
            phone_number='1234567892',
            team_name='management',
            is_superuser=False
        )
        self.user3 = CustomUserAccount.objects.create_user(
            username='support',
            password='admin',
            email='support@example.com',
            first_name='Support',
            last_name='User',
            phone_number='1234567893',
            team_name='support',
            is_superuser=False
        )
        self.user4 = CustomUserAccount.objects.create_user(
            username='sales',
            password='admin',
            email='sales@example.com',
            first_name='Sales',
            last_name='User',
            phone_number='1234567894',
            team_name='sales',
            is_superuser=False
        )
        #self.team = Team.objects.create(name='management')
        self.token1 = CustomToken.objects.create(user=self.user1)
        self.token2 = CustomToken.objects.create(user=self.user2)
        self.token3 = CustomToken.objects.create(user=self.user3)
        self.token4 = CustomToken.objects.create(user=self.user4)

        self.token1 = refresh_or_create_token(self.user1)
        self.token2 = refresh_or_create_token(self.user2)
        self.token3 = refresh_or_create_token(self.user3)
        self.token4 = refresh_or_create_token(self.user4)

    def test_list_users(self):
        call_command('authentication', '-login', stdout=self.out)
        self.assertIn('admin', self.out.getvalue())

    def test_list_users(self):
        call_command('authentication', '-login', stdout=self.out)
        self.assertIn('support', self.out.getvalue())

    def test_list_users(self):
        call_command('authentication', '-login', stdout=self.out)
        self.assertIn('manager', self.out.getvalue())

    def test_list_users(self):
        call_command('authentication', '-login', stdout=self.out)
        self.assertIn('sales', self.out.getvalue())

    def test_list_users(self):
        call_command('user', '-list', stdout=self.out)
        self.assertIn('admin', self.out.getvalue())

    def test_create_user(self):
        call_command('user', '-create', 'username=newuser', 'password=newpassword', 'email=newuser@example.com', 'first_name=New', 'last_name=User', 'phone_number=0987654321', 'team_name=sales', stdout=self.out)
        self.assertIn('Successfully created user', self.out.getvalue())

    def test_delete_user(self):
        call_command('user', '-delete', 'username=newuser', stdout=self.out)
        self.assertIn('Successfully deleted user', self.out.getvalue())

    def test_update_user(self):
        call_command('user', '-update', 'username=support', 'email=updatedsupport@example.com', stdout=self.out)
        self.assertIn('Successfully updated user', self.out.getvalue())

    def test_read_user(self):
        call_command('user', '-read', 'username=testuser', stdout=self.out)
        self.assertIn('Username: testuser', self.out.getvalue())

    def test_create_superuser(self):
        call_command('user', '-customcreatesuperuser', 'username=superuser', 'password=superpassword', 'email=superuser@example.com', 'first_name=Super', 'last_name=User', 'phone_number=1122334455', 'team_name=management', stdout=self.out)
        self.assertIn('Successfully created superuser', self.out.getvalue())

'''
# Python
from django.core.management import call_command
from django.test import TestCase
from CustomUser.models import CustomUserAccount, Team
from io import StringIO

class TestUserCommands(TestCase):
    def setUp(self):
        self.out = StringIO()
        self.err = StringIO()
        self.admin = CustomUserAccount.objects.create_superuser(username='admin', email='admin@example.com', password='admin')
        self.manager = CustomUserAccount.objects.create_user(username='manager', email='manager@example.com', password='manager', is_manager=True)
        self.user = CustomUserAccount.objects.create_user(username='user', email='user@example.com', password='user')
        self.team = Team.objects.create(name='sales')

    def test_create_user(self):
        call_command('user', '-create', 'current_user=admin', 'username=testuser', 'email=testuser@example.com', 'first_name=Test', 'last_name=User', 'phone_number=1234567890', 'team_name=sales', stdout=self.out, stderr=self.err)
        user = CustomUserAccount.objects.get(username='testuser')
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertEqual(user.phone_number, '1234567890')
        self.assertEqual(user.team.name, 'sales')

    def test_create_superuser(self):
        call_command('user', '-createsuperuser', 'current_user=admin', 'username=superuser', 'email=superuser@example.com', 'first_name=Super', 'last_name=User', 'phone_number=1234567890', 'team_name=sales', stdout=self.out, stderr=self.err)
        user = CustomUserAccount.objects.get(username='superuser')
        self.assertIsNotNone(user)
        self.assertTrue(user.is_superuser)
        self.assertEqual(user.email, 'superuser@example.com')
        self.assertEqual(user.first_name, 'Super')
        self.assertEqual(user.last_name, 'User')
        self.assertEqual(user.phone_number, '1234567890')
        self.assertEqual(user.team.name, 'sales')

    def test_list_users(self):
        call_command('user', '-list', 'current_user=admin', stdout=self.out, stderr=self.err)
        self.assertIn('testuser', self.out.getvalue())
        self.assertIn('superuser', self.out.getvalue())

    def test_delete_user(self):
        call_command('user', '-delete', 'current_user=admin', 'username=testuser', stdout=self.out, stderr=self.err)
        with self.assertRaises(CustomUserAccount.DoesNotExist):
            CustomUserAccount.objects.get(username='testuser')

    def test_update_user(self):
        call_command('user', '-update', 'current_user=admin', 'username=superuser', 'email=newemail@example.com', stdout=self.out, stderr=self.err)
        user = CustomUserAccount.objects.get(username='superuser')
        self.assertEqual(user.email, 'newemail@example.com')

    def test_read_user(self):
        call_command('user', '-read', 'current_user=admin', 'username=superuser', stdout=self.out, stderr=self.err)
        self.assertIn('superuser', self.out.getvalue())
        self.assertIn('newemail@example.com', self.out.getvalue())
'''