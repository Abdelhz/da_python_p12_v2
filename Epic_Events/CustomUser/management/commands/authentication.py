from getpass import getpass
from django.contrib.auth import get_user_model, authenticate
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from CustomUser.models import CustomToken

User = get_user_model()

class Command(BaseCommand):
    help = 'Manage user authentication'

    def add_arguments(self, parser):
        parser.add_argument('-login', action='store_true')
        parser.add_argument('-logout', action='store_true')
        parser.add_argument('-token', type=str)
        
        parser.add_argument('username', nargs='?', type=str)
        parser.add_argument('Current_user', nargs='?', type=str)

    def handle(self, *args, **options):
        if options['login']:
            self.login_user()
        elif options['logout']:
            self.logout_user()
        else:
            token = options['token']
            if not self.verify_token(token):
                raise CommandError('Invalid token')

    def login_user(self):
        username = options['username'] or input('Enter username: ')
        password = getpass('Enter password: ')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            token, created = CustomToken.objects.get_or_create(user=user)
            if not created:
                # If the token is not valid, refresh it
                if not self.verify_token(token):
                    token = token.refresh()
            print('Login successful.')
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

    def verify_token(self, token):
        if timezone.now() <= token.expires_at:
            return True
        return False