from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from Contract.models import Contract
from Client.models import Client
from CustomUser.models import CustomUserAccount
from CustomUser.permissions import IsAuthenticated, IsSuperuser, IsSameUser, IsManager
from Client.permissions import IsClientContact, IsSales
from Epic_Events.utils import get_signature_status, get_total_amount, get_remaining_amount

CONTRACT_FIELDS = ['current_user', 'client', 'contact_sales_EE', 'signature_status', 'total_amount', 'remaining_amount', 'contract_id']

CONTRACT_DESCRIPTIONS = {
    'current_user': "Enter current user's username: ",
    'client': "Enter client's full name: ",
    'signature_status': "Enter contract signature status: ",
    'total_amount': "Enter contract total amount: ",
    'remaining_amount': "Enter the amount remaining to pay : ",
}

class Command(BaseCommand):
    help = 'Command lines to manage CRUD operations on Contracts from the Contract model.'

    def add_arguments(self, parser):
        parser.add_argument('-list', action='store_true', help='List all contracts')
        parser.add_argument('-list_contact_contracts', action='store_true', help="List all the contracts that are not signed or not fully payed for.")
        parser.add_argument('-create', action='store_true', help='Create a new contract')
        parser.add_argument('-delete', action='store_true', help='Delete a contract')
        parser.add_argument('-update', action='store_true', help='Update a contract')
        parser.add_argument('-read', action='store_true', help='Read a contract details')
        
        for field in CONTRACT_FIELDS:
            parser.add_argument(field, nargs='?', type=str)

    def handle(self, *args, **options):
        if options['list']:
            self.list_contracts(options)
        elif options['list_contact_contracts']:
            self.list_contact_contracts(options)
        elif options['create']:
            self.create_contract(options)
        elif options['delete']:
            self.delete_contract(options)
        elif options['update']:
            self.update_contract(options)
        elif options['read']:
            self.read_contract(options)
        else:
            raise CommandError('Invalid command')


    def list_contracts(self, options):
        current_user_name = options['current_user'] or input(CONTRACT_DESCRIPTIONS['current_user'])
        try:
            current_user = CustomUserAccount.objects.get(username=current_user_name)
            permission = IsAuthenticated(current_user).has_permission()
        except CustomUserAccount.DoesNotExist:
            raise CommandError('Current user does not exist')
        
        if not permission:
            raise CommandError('You are not authenticated.')
        
        try:
            contracts = Contract.objects.all()
            if not contracts:
                self.stdout.write('No contracts exist.')
            else:
                for contract in contracts:
                    self.stdout.write(str(contract))
        except Exception as e:
            self.stdout.write('An error occurred: {}'.format(e))

    def list_contact_contracts(self, options):
        current_user_name = options['current_user'] or input(CONTRACT_DESCRIPTIONS['current_user'])
        try:
            current_user = CustomUserAccount.objects.get(username=current_user_name)
            permission = IsAuthenticated(current_user).has_permission() and IsSales(current_user).has_permission()
        except CustomUserAccount.DoesNotExist:
            raise CommandError('Current user does not exist')
        
        if not permission:
            raise CommandError('You are not authenticated and/or are a Management team member.')
        
        try:
            none_signed_contracts = Contract.objects.filter(signature_status=False)
            not_fully_payed_contracts = Contract.objects.filter(remaining_amount__gt=0)

            if not contracts:
                self.stdout.write('No contracts exist.')
            else:
                self.stdout.write("Contracts that are not signed : ")
                for none_signed_contract in none_signed_contracts:
                    self.stdout.write(str(none_signed_contract))
                
                self.stdout.write("Contracts that are not fully payed for : ")
                for not_fully_payed_contract in not_fully_payed_contracts:
                            self.stdout.write(str(not_fully_payed_contract))
        
        except Exception as e:
            self.stdout.write('An error occurred: {}'.format(e))

    def create_contract(self, options):
        current_user_name = options['current_user'] or input(CONTRACT_DESCRIPTIONS['current_user'])
        client_name = options['client'] or input(CONTRACT_DESCRIPTIONS['client'])
        
        signature_status = get_signature_status(options, CONTRACT_DESCRIPTIONS)
        total_amount = get_total_amount(options, CONTRACT_DESCRIPTIONS)
        remaining_amount = get_remaining_amount(options, CONTRACT_DESCRIPTIONS)

        try:
            current_user = CustomUserAccount.objects.get(username=current_user_name)
            client = Client.objects.get(full_name=client_name)
            permission = IsAuthenticated(current_user).has_permission() and IsManager(current_user).has_permission()
        
        except CustomUserAccount.DoesNotExist:
            raise CommandError('Current user or sales contact does not exist')
        except Client.DoesNotExist:
            raise CommandError('Client does not exist')

        if not permission:
            raise CommandError('You are not authenticated or you are not a member of the sales team.')
        
        try:
            with transaction.atomic():
                contract = Contract.objects.create_contract(client, total_amount, remaining_amount, signature_status)
                self.stdout.write(f'Successfully created contract {contract.unique_id} for client {client.full_name}')
        
        except Exception as e:
            raise CommandError(str(e))

    def delete_contract(self, options):
        current_user_name = options['current_user'] or input(CONTRACT_DESCRIPTIONS['current_user'])
        contract_id = options['contract_id'] or input("Enter contract's ID: ")

        try:
            current_user = CustomUserAccount.objects.get(username=current_user_name)
            contract = Contract.objects.get(unique_id=contract_id)
            permission = IsAuthenticated(current_user).has_permission() and IsManager(current_user).has_permission()
        
        except CustomUserAccount.DoesNotExist:
            raise CommandError('Current user does not exist')
        except Contract.DoesNotExist:
            raise CommandError('Contract does not exist')

        if not permission:
            raise CommandError('You do not have permission to delete this contract. You must be authenticated and a management team member.')

        try:
            contract.delete()
            self.stdout.write(f'Successfully deleted contract with ID {contract.unique_id}.')
        except Exception as e:
            self.stdout.write('An error occurred: {}'.format(e))

    def update_contract(self, options):
        current_user_name = options['current_user'] or input(CONTRACT_DESCRIPTIONS['current_user'])
        contract_id = options['contract_id'] or input("Enter contract's ID: ")

        try:
            current_user = CustomUserAccount.objects.get(username=current_user_name)
            contract = Contract.objects.get(unique_id=contract_id)
            permission = IsAuthenticated(current_user).has_permission() and (IsSameUser(contract.contact_sales_EE, current_user).has_permission() or IsManager(current_user).has_permission())
        
        except CustomUserAccount.DoesNotExist:
            raise CommandError('Current user does not exist')
        except Contract.DoesNotExist:
            raise CommandError('Contract does not exist')

        if not permission:
            raise CommandError('You do not have permission to update this contract.')

        with transaction.atomic():
            update_fields = {}
            for field in ['signature_status', 'total_amount', 'remaining_amount']:

                if field == 'total_amount':
                    value = get_total_amount(options, CONTRACT_DESCRIPTIONS)
                elif field == 'remaining_amount':
                    value = get_remaining_amount(options, CONTRACT_DESCRIPTIONS)
                elif field == 'signature_status':
                    value = get_signature_status(options, CONTRACT_DESCRIPTIONS)
                
                if value: # Check if value is not an empty string
                    update_fields[field] = value
            try:
                contract = Contract.objects.update_contract(contract, **update_fields)
                self.stdout.write(f'Successfully updated contract with ID {contract.unique_id}.')
            except Exception as e:
                self.stdout.write('An error occurred: {}'.format(e))


    def read_contract(self, options):
        current_user_name = options['current_user'] or input(CONTRACT_DESCRIPTIONS['current_user'])
        contract_id = options['contract_id'] or input("Enter contract's ID: ")

        try:
            current_user = CustomUserAccount.objects.get(username=current_user_name)
            permission = IsAuthenticated(current_user).has_permission()
        except CustomUserAccount.DoesNotExist:
            raise CommandError('Current user does not exist')

        if not permission:
            raise CommandError('You do not have permission to read this contract.')

        try:
            contract = Contract.objects.get(unique_id=contract_id)
            self.stdout.write(str(contract))
        except Contract.DoesNotExist:
            raise CommandError('Contract does not exist')
        except Exception as e:
            self.stdout.write('An error occurred: {}'.format(e))