from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Permission
from django.db import transaction
from getpass import getpass
from CustomUser.models import CustomUserAccount, Team


USER_FIELDS = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'team_name']

USER_DESCRIPTIONS = {
    'username': "Enter username: ",
    'email': "Enter email: ",
    'first_name': "Enter first name: ",
    'last_name': "Enter last name: ",
    'phone_number': "Enter phone number: ",
    'team_name': "Enter team name: ",
}


class Command(BaseCommand):
    help = 'Command lines to manage CRUD operations on Users from the CustomUserAccount model.'

    def add_arguments(self, parser):
        parser.add_argument('-list', action='store_true', help='List all users')
        parser.add_argument('-create', action='store_true', help='Create a new user')
        parser.add_argument('-delete', action='store_true', help='Delete a user')
        parser.add_argument('-update', action='store_true', help='Update a user')
        parser.add_argument('-read', action='store_true', help='Read a user details')
        parser.add_argument('-createsuperuser', action='store_true', help='Create a new superuser')
        for field in USER_FIELDS:
            parser.add_argument(field, nargs='?', type=str)


    def handle(self, *args, **options):
        if options['list']:
            self.list_users()
        elif options['create']:
            self.create_user(options)
        elif options['delete']:
            self.delete_user(options)
        elif options['update']:
            self.update_user(options)
        elif options['read']:
            self.read_user(options)
        elif options['createsuperuser']:
            self.create_superuser(options)
        else:
            raise CommandError('Invalid command')

def list_users(self):
    try:
        users = CustomUserAccount.objects.all()
        if not users:
            self.stdout.write('No users exist.')
        else:
            for user in users:
                self.stdout.write(str(user))
    except Exception as e:
        self.stdout.write('An error occurred: {}'.format(e))

    def create_user(self, options):
        username = options['username'] or input('Enter username: ')
        email = options['email'] or input('Enter email: ')
        first_name = options['first_name'] or input('Enter first name: ')
        last_name = options['last_name'] or input('Enter last name: ')
        phone_number = options['phone_number'] or input('Enter phone number: ')
        password = getpass('Enter password: ')
        team_name = options['team_name'] or input('Enter team name: ')
        try:
            with transaction.atomic():
                user = CustomUserAccount.objects.create_user(username, first_name, last_name, email, phone_number, password, team_name)
                self.stdout.write(f'Successfully created user {user}')
        except Exception as e:
            raise CommandError(str(e))


    def create_superuser(self, options):
        username = options['username'] or input('Enter username: ')
        email = options['email'] or input('Enter email: ')
        first_name = options['first_name'] or input('Enter first name: ')
        last_name = options['last_name'] or input('Enter last name: ')
        phone_number = options['phone_number'] or input('Enter phone number: ')
        password = getpass('Enter password: ')
        team_name = options['team_name'] or input('Enter team name: ')
        try:
            with transaction.atomic():
                user = CustomUserAccount.objects.create_superuser(username, email, first_name, last_name, phone_number, password, team_name)
                self.stdout.write(f'Successfully created superuser {user}')
        except Exception as e:
            raise CommandError(str(e))


    def delete_user(self, options):
        username = options['username'] or input('Enter username of user to delete: ')
        try:
            user = CustomUserAccount.objects.get(username=username)
            user.delete()
            self.stdout.write(f'Successfully deleted user {username}')
        except CustomUserAccount.DoesNotExist:
            raise CommandError('User does not exist')

    def update_user(self, options):
        username = options['username'] or input('Enter username of user to update: ')
        try:
            user = CustomUserAccount.objects.get(username=username)
            for field in ['email', 'first_name', 'last_name', 'phone_number', 'team_name']:
                value = options[field] or input(f'Enter new {field}: ')
                if field == 'team_name':
                    team = Team.objects.get(name=value)
                    user.team = team
                else:
                    setattr(user, field, value)
            user.save()
            self.stdout.write(f'Successfully updated user {user}')
        except CustomUserAccount.DoesNotExist:
            raise CommandError('User does not exist')
        except Team.DoesNotExist:
            raise CommandError('Team does not exist')

    def read_user(self, options):
        username = options['username'] or input('Enter username of user to read: ')
        try:
            user = CustomUserAccount.objects.get(username=username)
            self.stdout.write(str(user))
        except CustomUserAccount.DoesNotExist:
            raise CommandError('User does not exist')