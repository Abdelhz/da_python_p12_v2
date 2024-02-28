from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from Event.models import Event
from Contract.models import Contract
from Client.models import Client
from CustomUser.models import CustomUserAccount
from CustomUser.permissions import IsAuthenticated, IsSuperuser, IsSameUser, IsManager
from Client.permissions import IsClientContact, IsSales
from Event.permissions import IsSupport, IsEventContact
from Epic_Events.utils import get_attendees

EVENT_FIELDS = ['current_user', 'event_name', 'contract', 'contact_support_EE', 'date_start', 'date_end', 'location', 'attendees', 'notes']

EVENT_DESCRIPTIONS = {
    'event_name': "Enter event name: ",
    'contract': "Enter contract ID: ",
    'contact_support_EE': "Enter contact support EE's username: ",
    'date_start': "Enter event start date (YYYY-MM-DD HH:MM:SS): ",
    'date_end': "Enter event end date (YYYY-MM-DD HH:MM:SS): ",
    'location': "Enter event location: ",
    'attendees': "Enter number of attendees: ",
    'notes': "Enter event notes: ",
}

class Command(BaseCommand):
    help = 'Command lines to manage CRUD operations on Events from the Event model.'

    def add_arguments(self, parser):
        parser.add_argument('-list', action='store_true', help='List all events')
        parser.add_argument('-list_contact_events', action='store_true', help="List all the events that are assigned to the support team member.")
        parser.add_argument('-create', action='store_true', help='Create a new event')
        parser.add_argument('-delete', action='store_true', help='Delete an event')
        parser.add_argument('-update', action='store_true', help='Update an event')
        parser.add_argument('-read', action='store_true', help='Read an event details')
        
        for field in CONTRACT_FIELDS:
            parser.add_argument(field, nargs='?', type=str)

    def handle(self, *args, **options):
        if options['list']:
            self.list_events()
        elif options['list_contact_events']:
            self.list_contact_events(options)
        elif options['create']:
            self.create_event(options)
        elif options['delete']:
            self.delete_event(options)
        elif options['update']:
            self.update_event(options)
        elif options['read']:
            self.read_event(options)
        else:
            raise CommandError('Invalid command')


    def list_events(self):
        current_user_name = options['current_user'] or input(EVENT_DESCRIPTIONS['current_user'])
        try:
            current_user = CustomUserAccount.objects.get(username=current_user_name)
            permission = IsAuthenticated(current_user).has_permission()
        except CustomUserAccount.DoesNotExist:
            raise CommandError('Current user does not exist')
        
        if not permission:
            raise CommandError('You are not authenticated.')
        
        try:
            events = Event.objects.all()
            if not events:
                self.stdout.write('No events exist.')
            else:
                for event in events:
                    self.stdout.write(str(event))
        except Exception as e:
            self.stdout.write('An error occurred: {}'.format(e))

    def list_contact_events(self, options):
        current_user_name = options['current_user'] or input(EVENT_DESCRIPTIONS['current_user'])
        try:
            current_user = CustomUserAccount.objects.get(username=current_user_name)
            permission = IsAuthenticated(current_user).has_permission() and IsSupport(current_user).has_permission()
        except CustomUserAccount.DoesNotExist:
            raise CommandError('Current user does not exist')
        
        if not permission:
            raise CommandError('You are not authenticated and/or not a Support team member.')
        
        try:
            assigned_events = Event.objects.filter(contact_support_EE=current_user)

            if not events:
                self.stdout.write('No events exist.')
            else:
                self.stdout.write("Events that are assigned to the user : ")
                for assigned_event in assigned_events:
                    self.stdout.write(str(assigned_event))
        
        except Exception as e:
            self.stdout.write('An error occurred: {}'.format(e))

    def create_event(self, options):
        current_user_name = options['current_user'] or input(EVENT_DESCRIPTIONS['current_user'])

        try:
            current_user = CustomUserAccount.objects.get(username=current_user_name)
            #contact_support_EE = CustomUserAccount.objects.get(username=contact_support_EE_username)
            permission = IsAuthenticated(current_user).has_permission() and IsSales(current_user).has_permission()
        except CustomUserAccount.DoesNotExist:
            raise CommandError('Current user does not exist')
        
        if not permission:
            raise CommandError('You are not authenticated or you are not a member of the sales team.')

        contract_id = options['contract'] or input(EVENT_DESCRIPTIONS['contract'])

        try:
            contract = Contract.objects.get(contract_id=contract_id)
            client = contract.client
            permissions = IsClientContact(current_user, client).has_permission()
        except Contract.DoesNotExist:
            raise CommandError('Contract does not exist')
        except Client.DoesNotExist:
            raise CommandError('Client does not exist')
        
        if not permissions:
            raise CommandError("You are not the client's contact for this contract.")
        
        if not contract.signature_status:
            raise CommandError('This contract is not signed yet.')
        
        event_name = options['event_name'] or input(EVENT_DESCRIPTIONS['event_name'])
        date_start = options['date_start'] or input(EVENT_DESCRIPTIONS['date_start'])
        date_end = options['date_end'] or input(EVENT_DESCRIPTIONS['date_end'])
        location = options['location'] or input(EVENT_DESCRIPTIONS['location'])
        notes = options['notes'] or input(EVENT_DESCRIPTIONS['notes'])
        
        attendees = get_attendees(options)
        
        try:
            with transaction.atomic():
                event = Event.objects.create_event(event_name, contract, date_end, date_start, location, attendees, notes)
                self.stdout.write(f'Successfully created contract {contract.id} for client {client.full_name}')
        
        except Exception as e:
            raise CommandError(str(e))

    def delete_event(self, options):
        current_user_name = options['current_user'] or input(EVENT_DESCRIPTIONS['current_user'])
        contract_id = options['id'] or input("Enter contract's ID: ")

        try:
            current_user = CustomUserAccount.objects.get(username=current_user_name)
            contract = Contract.objects.get(unique_id=contract_id)
            client = contract.client
            event = Event.objects.get(contract=contract)
            permission = IsAuthenticated(current_user).has_permission() and IsClientContact(current_user, client).has_permission()
        
        except CustomUserAccount.DoesNotExist:
            raise CommandError('Current user does not exist')
        except Contract.DoesNotExist:
            raise CommandError('Contract does not exist')
        except Client.DoesNotExist:
            raise CommandError('Client does not exist')
        except Event.DoesNotExist:
            raise CommandError('Event does not exist')

        if not permission:
            raise CommandError("You do not have permission to delete this Event. You must be authenticated and the sales team member responsible for the event's client.")

        try:
            event.delete()
            self.stdout.write(f'Successfully deleted contract with ID {contract.id}.')
        except Exception as e:
            self.stdout.write('An error occurred: {}'.format(e))

    def update_event(self, options):
        current_user_name = options['current_user'] or input(EVENT_DESCRIPTIONS['current_user'])
        contract_id = options['id'] or input("Enter contract's ID: ")
        contact_support_EE_username = options['contact_support_EE'] or input(EVENT_DESCRIPTIONS['contact_support_EE'])

        try:
            current_user = CustomUserAccount.objects.get(username=current_user_name)
            contract = Contract.objects.get(unique_id=contract_id)
            event = Event.objects.get(contract=contract)
            permission = IsAuthenticated(current_user).has_permission() and (IsManager(current_user).has_permission() or IsEventContact(current_user, event).has_permission())
        
        except CustomUserAccount.DoesNotExist:
            raise CommandError('Current user does not exist')
        except Contract.DoesNotExist:
            raise CommandError('Contract does not exist')
        except Event.DoesNotExist:
            raise CommandError('Event does not exist')

        if not permission:
            raise CommandError('You do not have permission to update this Event.')

        if IsManager(current_user).has_permission():
            fields = ['contact_support_EE']
        elif IsEventContact(current_user, event).has_permission():
            fields = ['event_name', 'date_start', 'date_end', 'location', 'attendees', 'notes']
        
        with transaction.atomic():
            update_fields = {}
            for field in fields:
                value = options[field] or input(f'Enter new {field}: ')
                if value: # Check if value is not an empty string
                    if field == 'contact_support_EE':
                        try:
                            contact_support_EE = CustomUserAccount.objects.get(username=value)
                            permission = IsSupport(contact_support_EE).has_permission()
                        except CustomUserAccount.DoesNotExist:
                            raise CommandError('Epic Events Support team member does not exist')
                        if not permission:
                            raise CommandError('contact_support_EE is not a support team member.')
                        value = contact_support_EE
                    elif field == 'attendees':
                        value = get_attendees(options)
                    update_fields[field] = value

            event = Event.objects.update_event(client, **update_fields)
            self.stdout.write(f'Successfully updated Event {event.name}')


    def read_event(self, options):
        current_user_name = options['current_user'] or input(EVENT_DESCRIPTIONS['current_user'])
        contract_id = options['id'] or input("Enter contract's ID: ")
    
        try:
            current_user = CustomUserAccount.objects.get(username=current_user_name)
            contract = Contract.objects.get(unique_id=contract_id)
            permission = IsAuthenticated(current_user).has_permission()
        except CustomUserAccount.DoesNotExist:
            raise CommandError('Current user does not exist')
        except Contract.DoesNotExist:
            raise CommandError('Contract does not exist')

        if not permission:
            raise CommandError('You are not authenticated.')

        try:
            event = Event.objects.get(contract=contract)
            self.stdout.write(str(event))
        except Contract.DoesNotExist:
            raise CommandError('Contract does not exist')
        except Exception as e:
            self.stdout.write('An error occurred: {}'.format(e))