from django.core.management import call_command
from django.test import TestCase
from django.core.management.base import CommandError
from CustomUser.models import CustomUserAccount, Team, CustomToken
from Client.models import Client
from Contract.models import Contract
from Epic_Events.utils import refresh_or_create_token, verify_token

class ContractCommandTestCase(TestCase):
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

    def setUp(self):
        self.user = CustomUserAccount.objects.create(username='testuser')
        self.client = Client.objects.create(full_name='testclient')
        self.contract = Contract.objects.create(client=self.client, total_amount=100, remaining_amount=50, signature_status=False)

    def test_list_contracts(self):
        with self.assertLogs() as cm:
            call_command('contract', '-list', 'current_user=admin')
        self.assertIn(str(self.contract), cm.output)

    def test_list_contact_contracts(self):
        with self.assertLogs() as cm:
            call_command('contract', '-list_contact_contracts', 'current_user=sales')
        self.assertIn(str(self.contract), cm.output)

    def test_create_contract(self):
        with self.assertRaises(CommandError):
            call_command('contract', '-create', 'current_user=admin', 'client=testclient2', 'total_amount=200', 'remaining_amount=100', 'signature_status=True')
        self.assertEqual(Contract.objects.count(), 1)
        call_command('contract', '-create', 'current_user=testuser', 'client=testclient', 'total_amount=200', 'remaining_amount=100', 'signature_status=True')
        self.assertEqual(Contract.objects.count(), 2)

    def test_delete_contract(self):
        with self.assertRaises(CommandError):
            call_command('contract', '-delete', 'current_user=sales', 'contract_id=invalid_id')
        self.assertEqual(Contract.objects.count(), 1)
        call_command('contract', '-delete', 'current_user=testuser', 'contract_id=' + str(self.contract.unique_id))
        self.assertEqual(Contract.objects.count(), 0)

    def test_update_contract(self):
        with self.assertRaises(CommandError):
            call_command('contract', '-update', 'current_user=sales', 'contract_id=invalid_id', 'total_amount=150', 'remaining_amount=75', 'signature_status=True')
        self.assertEqual(self.contract.total_amount, 100)
        self.assertEqual(self.contract.remaining_amount, 50)
        self.assertEqual(self.contract.signature_status, False)
        call_command('contract', '-update', 'current_user=sales', 'contract_id=' + str(self.contract.unique_id), 'total_amount=150', 'remaining_amount=75', 'signature_status=True')
        self.contract.refresh_from_db()
        self.assertEqual(self.contract.total_amount, 150)
        self.assertEqual(self.contract.remaining_amount, 75)
        self.assertEqual(self.contract.signature_status, True)

    def test_read_contract(self):
        with self.assertLogs() as cm:
            call_command('contract', '-read', 'current_user=sales', 'contract_id=' + str(self.contract.unique_id))
        self.assertIn(str(self.contract), cm.output)