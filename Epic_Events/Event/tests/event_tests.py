from django.core.management import call_command
from django.test import TestCase
from CustomUser.models import CustomUserAccount, Team, CustomToken
from Client.models import Client
from Contract.models import Contract
from Event.models import Event
from Epic_Events.utils import refresh_or_create_token, verify_token

class CommandTestCase(TestCase):
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
        
        self.contract1 = Contract.objects.create(client=self.client, unique_id='testcontract1', signature_status=True)
        self.contract2 = Contract.objects.create(client=self.client2, unique_id='testcontract2', signature_status=True)
        self.contract3 = Contract.objects.create(client=self.client3, unique_id='testcontract3', signature_status=True)
        self.event1 = Event.objects.create(contract=self.contract1, event_name='testevent1')
        self.event2 = Event.objects.create(contract=self.contract2, event_name='testevent2')
        self.event3 = Event.objects.create(contract=self.contract3, event_name='testevent3')

    def test_handle(self):
        # Test list events
        call_command('command', '-list', current_user=self.user.username)
        self.assertIn('testevent', self.stdout.getvalue())

        # Test list contact events
        call_command('command', '-list_contact_events', current_user=self.user.username)
        self.assertIn('testevent', self.stdout.getvalue())

        # Test read event
        call_command('command', '-read', current_user=self.user.username, contract_id=self.contract.unique_id)
        self.assertIn('testevent', self.stdout.getvalue())

        # Test delete event
        call_command('command', '-delete', current_user=self.user.username, contract_id=self.contract.unique_id)
        self.assertNotIn('testevent', self.stdout.getvalue())

        # Test create event
        call_command('command', '-create', current_user=self.user.username, contract_id=self.contract.unique_id, event_name='newevent')
        self.assertIn('newevent', self.stdout.getvalue())

        # Test update event
        call_command('command', '-update', current_user=self.user.username, contract_id=self.contract.unique_id, event_name='updatedevent')
        self.assertIn('updatedevent', self.stdout.getvalue())