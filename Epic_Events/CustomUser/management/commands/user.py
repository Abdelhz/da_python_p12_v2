from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Permission
from django.db import transaction
from getpass import getpass
from CustomUser.models import CustomUserAccount, Team
from CustomUser.permissions import IsAuthenticated, IsSuperuser, IsSameUser


USER_FIELDS = ['current_user', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'team_name']

USER_DESCRIPTIONS = {
    'current_user': "Enter current user's username: ",
    'username': "Enter username: ",
    'email': "Enter email: ",
    'first_name': "Enter first name: ",
    'last_name': "Enter last name: ",
    'phone_number': "Enter phone number: ",
    'team_name': "Enter team name: ",
}

valid_team_names = ['sales', 'management', 'support']

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
        current_user_name = options['current_user'] or input("Enter current user's username: ")
        try:
            current_user = CustomUserAccount.objects.get(username=current_user_name)
            permission = IsAuthenticated(current_user).has_permission()
            
            if not permission:
                raise CommandError('You are not authenticated')

            users = CustomUserAccount.objects.all()
            
            if not users:
                self.stdout.write('No users exist.')
            else:
                for user in users:
                    self.stdout.write(f'Username: {user.username}, First Name: {user.first_name}, Last Name: {user.last_name}, Last Login: {user.last_login}')
        except Exception as e:
            self.stdout.write('An error occurred: {}'.format(e))
        except CustomUserAccount.DoesNotExist:
            raise CommandError('User does not exist')

    def create_user(self, options):
        current_user_name = options['current_user'] or input(USER_DESCRIPTIONS['current_user'])
        username = options['username'] or input(USER_DESCRIPTIONS['username'])
        email = options['email'] or input(USER_DESCRIPTIONS['email'])
        first_name = options['first_name'] or input(USER_DESCRIPTIONS['first_name'])
        last_name = options['last_name'] or input(USER_DESCRIPTIONS['last_name'])
        phone_number = options['phone_number'] or input(USER_DESCRIPTIONS['phone_number'])
        password = getpass('Enter password: ')
        
        team_name = (options['team_name'] or input(USER_DESCRIPTIONS['team_name'])).lower()
        while team_name not in valid_team_names:
            print(f'Invalid team name: {team_name}. Valid team_name options are : {", ".join(valid_team_names)}')
            team_name = input(USER_DESCRIPTIONS['team_name']).lower()
        
        try:
            current_user = CustomUserAccount.objects.get(username=current_user_name)
            permission = IsAuthenticated(current_user).has_permission() and (IsSuperuser(current_user).has_permission() or IsManager(current_user).has_permission())
            if not permission:
                raise CommandError('Current user is not authenticated and/or does not have permission to create a new user')
        except CustomUserAccount.DoesNotExist:
            raise CommandError('Current user does not exist')
        
        try:
            with transaction.atomic():
                user = CustomUserAccount.objects.create_user(username, first_name, last_name, email, phone_number, password, team_name)
                self.stdout.write(f'Successfully created user {user}')
        except Exception as e:
            raise CommandError(str(e))


    def create_superuser(self, options):
        current_user_name = options['current_user'] or input(USER_DESCRIPTIONS['current_user'])
        username = options['username'] or input(USER_DESCRIPTIONS['username'])
        email = options['email'] or input(USER_DESCRIPTIONS['email'])
        first_name = options['first_name'] or input(USER_DESCRIPTIONS['first_name'])
        last_name = options['last_name'] or input(USER_DESCRIPTIONS['last_name'])
        phone_number = options['phone_number'] or input(USER_DESCRIPTIONS['phone_number'])
        password = getpass('Enter password: ')
        
        team_name = (options['team_name'] or input(USER_DESCRIPTIONS['team_name'])).lower()
        while team_name not in valid_team_names:
            print(f'Invalid team name: {team_name}. Valid team_name options are : {", ".join(valid_team_names)}')
            team_name = input(USER_DESCRIPTIONS['team_name']).lower()
        
        try:
            current_user = CustomUserAccount.objects.get(username=current_user_name)
            permission = IsAuthenticated(current_user).has_permission() and IsSuperuser(current_user).has_permission()
            if not permission:
                if not IsAuthenticated(current_user).has_permission():
                    raise CommandError('Current user is not authenticated')
                elif not IsSuperuser(current_user).has_permission() and CustomUserAccount.objects.filter(is_superuser=True).exists():
                    raise CommandError('Current user is not a superuser and does not have permission to create a new user')
        except CustomUserAccount.DoesNotExist:
            raise CommandError('Current user does not exist')
        
        try:
            with transaction.atomic():
                user = CustomUserAccount.objects.create_superuser(username, email, first_name, last_name, phone_number, password, team_name)
                self.stdout.write(f'Successfully created superuser {user}')
        except Exception as e:
            raise CommandError(str(e))


    def delete_user(self, options):
        current_user_name = options['current_user'] or input(USER_DESCRIPTIONS['current_user'])
        username = options['username'] or input('Enter username of user to delete: ')
        try:
            current_user = CustomUserAccount.objects.get(username=current_user_name)
            user = CustomUserAccount.objects.get(username=username)
            permission = IsAuthenticated(current_user).has_permission() and (IsSuperuser(current_user).has_permission() or IsSameUser(user, current_user) or IsManager(current_user).has_permission())
            
            if permission:
                user.delete()
                self.stdout.write(f'Successfully deleted user {username}')
        except CustomUserAccount.DoesNotExist:
            raise CommandError('User does not exist')

    def update_user(self, options):
        current_user_name = options['current_user'] or input(USER_DESCRIPTIONS['current_user'])
        username = options['username'] or input('Enter username of user to update: ')
        try:
            current_user = CustomUserAccount.objects.get(username=current_user_name)
            user = CustomUserAccount.objects.get(username=username)
            Permission = IsAuthenticated(current_user).has_permission() and (IsSuperuser(current_user).has_permission() or IsSameUser(user, current_user) or IsManager(current_user).has_permission())
            
            if Permission:
                with transaction.atomic():
                    for field in ['email', 'first_name', 'last_name', 'phone_number', 'team_name']:
                        value = options[field] or input(f'Enter new {field}: ')
                        if valut: # Check if value is not an empty string
                            if field == 'team_name':
                                team_name = value.lower()
                                while team_name not in valid_team_names:
                                    print(f'Invalid team name: {team_name}. Valid team_name options are : {", ".join(valid_team_names)}')
                                    team_name = input(USER_DESCRIPTIONS['team_name']).lower()
                                try:
                                    team = Team.objects.get(name=team_name)
                                except Team.DoesNotExist:
                                    raise CommandError(f'Team {team_name} does not exist')
                                user.team = team
                            else:
                                setattr(user, field, value)
                    user.save()
                    self.stdout.write(f'Successfully updated user {user}')
        except CustomUserAccount.DoesNotExist:
            raise CommandError('User does not exist')

    def read_user(self, options):
        current_user_name = options['current_user'] or input(USER_DESCRIPTIONS['current_user'])
        username = options['username'] or input('Enter username of user to read: ')
        try:
            current_user = CustomUserAccount.objects.get(username=current_user_name)
            permission = IsAuthenticated(current_user).has_permission()
            
            if permission:
                user = CustomUserAccount.objects.get(username=username)
                user_info = f"Username: {user.username}\n, Last Name: {user.last_name}\n, First Name: {user.first_name}\n, Email: {user.email}, Team Name: {user.team.name}\n, Date Joined: {user.date_joined}\n, Last Login: {user.last_login}\n"
                self.stdout.write(user_info)
        except CustomUserAccount.DoesNotExist:
            raise CommandError('User does not exist')