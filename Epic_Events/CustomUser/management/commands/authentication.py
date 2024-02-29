from getpass import getpass
from django.contrib.auth import get_user_model, authenticate
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from CustomUser.models import CustomToken
from Epic_Events.utils import refresh_or_create_token, verify_token

#! CLean code here "User = get_user_model()" ?
User = get_user_model()

class Command(BaseCommand):
    help = 'Manage user authentication'

    def add_arguments(self, parser):
        parser.add_argument('-login', action='store_true')
        parser.add_argument('-logout', action='store_true')
        parser.add_argument('-token', type=str) #! Not needed.
        
        parser.add_argument('username', nargs='?', type=str)
        parser.add_argument('Current_user', nargs='?', type=str)

    def handle(self, *args, **options):
        if options['login']:
            self.login_user(options)
        elif options['logout']:
            self.logout_user(options)
        else:
            pass

    def login_user(self, options):

        username = options['username'] or input('Enter username: ')
        password = getpass('Enter password: ')
        user = authenticate(username=username, password=password)

        if user is not None:
            try:
                token = refresh_or_create_token(user)
                user.last_login = timezone.now()  # Update the last_login field
                user.save()  # Save the user instance
                print('Login successful.')
            except Exception as e:
                print(f'An error occurred: {e}')
        else:
            print('Login failed. username or password is incorrect.')

    def logout_user(self, options):
        
        username = options['username'] or input('Enter username: ')
        password = getpass('Enter password: ')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            try:
                token = CustomToken.objects.get(user=user)
                token.delete()
                print('Logout successful')
            except Token.DoesNotExist:
                print('Invalid token')
        else:
            print('Failed to logout. Unauthenticated user.')