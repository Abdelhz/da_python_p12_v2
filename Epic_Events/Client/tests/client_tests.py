from django.core.management import call_command
from django.test import TestCase
from django.contrib.auth import get_user_model
from Client.models import Client
from CustomUser.models import CustomUserAccount, Team, CustomToken
from Epic_Events.utils import refresh_or_create_token, verify_token

User = get_user_model()

class TestCommands(TestCase):
    
    
    def setUp(self):
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
            username='sales',
            password='admin',
            email='sales@example.com',
            first_name='sales',
            last_name='User',
            phone_number='1234567',
            team_name='sales',
        )

        self.user3 = CustomUserAccount.objects.create_user(
            username='admin',
            password='admin',
            email='support@example.com',
            first_name='support',
            last_name='User',
            phone_number='123467891',
            team_name='support',
        )

        self.client = Client.objects.create(
            current_user=self.user2,
            full_name='Test Client1',
            email='testclient1@example.com',
            phone_number='123457890',
            company_name='Test Company1',
            contact_sales_EE=self.user2,
            information='Test Information'
        )

        self.client2 = Client.objects.create(
            current_user=self.user2,
            full_name='Test Client1',
            email='testclient2@example.com',
            phone_number='123456789',
            company_name='Test Company2',
            contact_sales_EE=self.user2,
            information='Test Information'
        )

        self.client3 = Client.objects.create(
            current_user=self.user2,
            full_name='Test Client1',
            email='testclient3@example.com',
            phone_number='12567890',
            company_name='Test Company3',
            contact_sales_EE=self.user2,
            information='Test Information'
        )
        self.token1 = CustomToken.objects.create(user=self.user1)
        self.token2 = CustomToken.objects.create(user=self.user2)
        self.token3 = CustomToken.objects.create(user=self.user3)

        self.token1 = refresh_or_create_token(self.user1)
        self.token2 = refresh_or_create_token(self.user2)
        self.token3 = refresh_or_create_token(self.user3)

    def test_list_clients(self):
        call_command('client', '-list', current_user='testuser')
        # Add assertions here to check the output

    def test_create_client(self):
        call_command('client', '-create', current_user='testuser', full_name='New Client', email='newclient@example.com', phone_number='0987654321', company_name='New Company', information='New Information')
        # Add assertions here to check if the client was created

    def test_delete_client(self):
        call_command('client', '-delete', current_user='testuser', full_name='Test Client')
        # Add assertions here to check if the client was deleted

    def test_update_client(self):
        call_command('client', '-update', current_user='testuser', full_name='Test Client', email='updatedclient@example.com')
        # Add assertions here to check if the client was updated

    def test_read_client(self):
        call_command('client', '-read', current_user='testuser', full_name='Test Client')
        # Add assertions here to check the output