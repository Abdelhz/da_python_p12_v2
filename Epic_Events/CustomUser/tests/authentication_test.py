# Python
import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from django.utils import timezone
from CustomUser.models import CustomUserAccount, CustomToken
from Epic_Events.utils import refresh_or_create_token

@pytest.fixture
def create_user():
    return CustomUserAccount.objects.create(username='testuser', password='testpassword')

@pytest.mark.django_db
def test_login_user(create_user):
    call_command('authentication', '-login', username=create_user.username)
    assert CustomToken.objects.filter(user=create_user).exists()

@pytest.mark.django_db
def test_logout_user(create_user):
    call_command('authentication', '-logout', username=create_user.username)
    assert not CustomToken.objects.filter(user=create_user).exists()

@pytest.mark.django_db
def test_invalid_command(create_user):
    with pytest.raises(CommandError):
        call_command('authentication', '-invalid', username=create_user.username)

from django.test import TestCase
from django.core.management import call_command
from django.contrib.auth import get_user_model
from unittest.mock import patch, MagicMock
from io import StringIO

User = get_user_model()

class AuthenticationCommandTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    @patch('getpass.getpass')
    @patch('builtins.input')
    def test_login_user(self, mock_input, mock_getpass):
        mock_input.return_value = 'testuser'
        mock_getpass.return_value = '12345'

        out = StringIO()
        call_command('authentication', '-login', stdout=out)
        self.assertIn('Login successful.', out.getvalue())

    @patch('getpass.getpass')
    @patch('builtins.input')
    def test_login_user_fail(self, mock_input, mock_getpass):
        mock_input.return_value = 'wronguser'
        mock_getpass.return_value = 'wrongpass'

        out = StringIO()
        call_command('authentication', '-login', stdout=out)
        self.assertIn('Login failed. username or password is incorrect.', out.getvalue())

    @patch('getpass.getpass')
    @patch('builtins.input')
    def test_logout_user(self, mock_input, mock_getpass):
        mock_input.return_value = 'testuser'
        mock_getpass.return_value = '12345'

        # First, we need to login the user to generate a token
        call_command('authentication', '-login')

        out = StringIO()
        call_command('authentication', '-logout', stdout=out)
        self.assertIn('Logout successful', out.getvalue())