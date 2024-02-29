from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Permission
from django.db import transaction
from Client.models import Client
from CustomUser.models import CustomUserAccount
from CustomUser.permissions import IsAuthenticated, IsSuperuser, IsSameUser
from Client.permissions import IsClientContact, IsSales


CLIENT_FIELDS = ['current_user', 'full_name', 'email', 'phone_number', 'company_name', 'contact_sales_EE', 'information']


CLIENT_DESCRIPTIONS = {
    'current_user': "Enter current user's username: ",
    'full_name': "Enter client's full name: ",
    'email': "Enter client's email: ",
    'phone_number': "Enter client's phone number: ",
    'company_name': "Enter client's company name: ",
    'contact_sales_EE': "Enter Epic Events contact's username: ",
    'information': "Enter additional information: ",
}

class Command(BaseCommand):
    help = 'Command lines to manage CRUD operations on Clients from the Client model.'

    def add_arguments(self, parser):
        parser.add_argument('-list', action='store_true', help='List all clients')
        parser.add_argument('-list_contact_clients', action='store_true', help="List all the current user's clients.")
        parser.add_argument('-create', action='store_true', help='Create a new client')
        parser.add_argument('-delete', action='store_true', help='Delete a client')
        parser.add_argument('-update', action='store_true', help='Update a client')
        parser.add_argument('-read', action='store_true', help='Read a client details')
        
        for field in CLIENT_FIELDS:
            parser.add_argument(field, nargs='?', type=str)

    def handle(self, *args, **options):
        if options['list']:
            self.list_clients(options)
        elif options['list_contact_clients']:
            self.list_clients_contact(options)
        elif options['create']:
            self.create_client(options)
        elif options['delete']:
            self.delete_client(options)
        elif options['update']:
            self.update_client(options)
        elif options['read']:
            self.read_client(options)
        else:
            raise CommandError('Invalid command')

    def list_clients(self, options):
        
        current_user_name = options['current_user'] or input(CLIENT_DESCRIPTIONS['current_user'])
        
        try:
            current_user = CustomUserAccount.objects.get(username=current_user_name)
            permission = IsAuthenticated(current_user).has_permission()
        except CustomUserAccount.DoesNotExist:
            raise CommandError('Current user does not exist')
        
        if not permission:
            raise CommandError('You are not authenticated.')
        
        try:
            clients = Client.objects.all()
            if not clients:
                self.stdout.write('No clients exist.')
            else:
                for client in clients:
                    self.stdout.write(str(client))
        except Exception as e:
            self.stdout.write('An error occurred: {}'.format(e))
    

    def list_clients_contact(self, options):
        current_user_name = options['current_user'] or input(CLIENT_DESCRIPTIONS['current_user'])
        try:
            current_user = CustomUserAccount.objects.get(username=current_user_name)
            permission = IsAuthenticated(current_user).has_permission() and IsSales(current_user).has_permission()
        except CustomUserAccount.DoesNotExist:
            raise CommandError('Current user does not exist')
        
        if not permission:
            raise CommandError('You are not authenticated.')
        
        try:
            clients = Client.objects.filter(contact_sales_EE=current_user)
            if not clients:
                self.stdout.write('No clients exist.')
            else:
                for client in clients:
                    self.stdout.write(str(client))
        except Exception as e:
            self.stdout.write('An error occurred: {}'.format(e))


    def create_client(self, options):
        current_user_name = options['current_user'] or input(CLIENT_DESCRIPTIONS['current_user'])
        full_name = options['full_name'] or input(CLIENT_DESCRIPTIONS['full_name'])
        email = options['email'] or input(CLIENT_DESCRIPTIONS['email'])
        phone_number = options['phone_number'] or input(CLIENT_DESCRIPTIONS['phone_number'])
        company_name = options['company_name'] or input(CLIENT_DESCRIPTIONS['company_name'])
        information = options['information'] or input(CLIENT_DESCRIPTIONS['information'])

        try:
            current_user = CustomUserAccount.objects.get(username=current_user_name)
            permission = IsAuthenticated(current_user).has_permission() and IsSales(current_user).has_permission()
        except CustomUserAccount.DoesNotExist:
            raise CommandError('Current user does not exist')

        if not permission:
            raise CommandError('You are not authenticated or you are not a member of the sales team.')
        
        try:
            with transaction.atomic():
                contact_sales_EE = current_user

                client = Client.objects.create_client(full_name, email, phone_number, company_name, contact_sales_EE, information)
                self.stdout.write(f'Successfully created client {client.full_name}')
        
        except Exception as e:
            raise CommandError(str(e))

    def delete_client(self, options):
        current_user_name = options['current_user'] or input(CLIENT_DESCRIPTIONS['current_user'])
        full_name = options['full_name'] or input('Enter full name of client to delete: ')
        try:
            current_user = CustomUserAccount.objects.get(username=current_user_name)
            permission = IsAuthenticated(current_user).has_permission() and IsSales(current_user).has_permission() and IsSuperuser(current_user).has_permission()
        except CustomUserAccount.DoesNotExist:
            raise CommandError('Current user does not exist')
        
        if not permission:
            raise CommandError('You are not authenticated or you are not a member of the sales team.')

        try:
            client = Client.objects.get(full_name=full_name)
            client.delete()
            self.stdout.write(f'Successfully deleted client {full_name}')
        except Client.DoesNotExist:
            raise CommandError('Client does not exist')

    def update_client(self, options):
        current_user_name = options['current_user'] or input(CLIENT_DESCRIPTIONS['current_user'])
        
        full_name = options['full_name'] or input('Enter full name of client to update: ')
        
        try:
            current_user = CustomUserAccount.objects.get(username=current_user_name)
            client = Client.objects.get(full_name=full_name)
            permission = IsAuthenticated(current_user).has_permission() and IsSales(current_user).has_permission() and IsClientContact(current_user, client).has_permission()
        except CustomUserAccount.DoesNotExist:
            raise CommandError('Current user does not exist')
        except Client.DoesNotExist:
            raise CommandError('Client does not exist')

        if not permission:
            raise CommandError("You are not authenticated or you are not the client's contact")
        
        with transaction.atomic():
            update_fields = {}
            for field in ['email', 'full_name', 'phone_number', 'company_name', 'contact_sales_EE', 'information']:
                value = options[field] or input(f'Enter new {field}: ')
                if value: # Check if value is not an empty string
                    if field == 'contact_sales_EE':
                        try:
                            contact_sales_EE = CustomUserAccount.objects.get(username=value)
                        except CustomUserAccount.DoesNotExist:
                            raise CommandError(f'Epic Events contact {value} does not exist')
                        value = contact_sales_EE
                    update_fields[field] = value

            client = Client.objects.update_client(client, **update_fields)
            self.stdout.write(f'Successfully updated client {client.full_name}')

    def read_client(self, options):
        current_user_name = options['current_user'] or input(CLIENT_DESCRIPTIONS['current_user'])
        
        full_name = options['full_name'] or input('Enter full name of client to read: ')
        
        try:
            current_user = CustomUserAccount.objects.get(username=current_user_name)
            permission = IsAuthenticated(current_user).has_permission()
        except CustomUserAccount.DoesNotExist:
            raise CommandError('Current user does not exist')
        
        if not permission:
            raise CommandError("You are not authenticated or you are not the client's contact")
        try:
            client = Client.objects.get(full_name=full_name)
            client_info = f"Full Name: {client.full_name}\n, Email: {client.email}\n, Phone Number: {client.phone_number}\n, Company Name: {client.company_name}\n, Epic Events Contact: {client.contact_sales_EE.username}\n, Information: {client.information}\n"
            self.stdout.write(client_info)
        except Client.DoesNotExist:
            raise CommandError('Client does not exist')
