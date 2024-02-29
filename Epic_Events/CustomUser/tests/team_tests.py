# Python
from django.core.management import call_command
from django.test import TestCase
from CustomUser.models import Team, CustomUserAccount
from django.core.management import call_command
from django.core.management.base import CommandError
from unittest.mock import patch

class TeamCommandTest(TestCase):
    def setUp(self):
        self.user = CustomUserAccount.objects.create_user(username='testuser', password='testpassword', is_superuser=True)
        self.team_name = 'sales'

    def test_create_team(self):
        # Act
        call_command('team', '-create', 'team_name=' + self.team_name, 'current_user=' + self.user.username)

        # Assert
        team = Team.objects.get(name=self.team_name)
        self.assertIsNotNone(team)

    def test_list_teams(self):
        # Arrange
        call_command('team', '-create', 'team_name=' + self.team_name, 'current_user=' + self.user.username)

        # Act
        output = call_command('team', '-list', 'current_user=' + self.user.username)

        # Assert
        self.assertIn(self.team_name, output)

    def test_read_team(self):
        # Arrange
        call_command('team', '-create', 'team_name=' + self.team_name, 'current_user=' + self.user.username)

        # Act
        output = call_command('team', '-read', 'team_name=' + self.team_name, 'current_user=' + self.user.username)

        # Assert
        self.assertIn(self.team_name, output)

    def test_delete_team(self):
        # Arrange
        call_command('team', '-create', 'team_name=' + self.team_name, 'current_user=' + self.user.username)

        # Act
        call_command('team', '-delete', 'team_name=' + self.team_name, 'current_user=' + self.user.username)

        # Assert
        with self.assertRaises(Team.DoesNotExist):
            Team.objects.get(name=self.team_name)



class CommandTestCase(TestCase):
    def setUp(self):
        self.superuser = CustomUserAccount.objects.create_superuser(username='superuser', password='password')
        self.user = CustomUserAccount.objects.create_user(username='user', password='password')
        self.team = Team.objects.create(name='sales')

    def test_list_teams(self):
        with patch('builtins.input', return_value='superuser'):
            call_command('team', '-list')

    def test_create_team(self):
        with patch('builtins.input', return_value='superuser'):
            call_command('team', '-create', 'management')

    def test_delete_team(self):
        with patch('builtins.input', return_value='superuser'):
            call_command('team', '-delete', 'sales')

    def test_read_team(self):
        with patch('builtins.input', return_value='superuser'):
            call_command('team', '-read', 'sales')

    def test_invalid_command(self):
        with self.assertRaises(CommandError):
            call_command('team', '-invalid')

    def test_create_team_without_permission(self):
        with self.assertRaises(CommandError):
            with patch('builtins.input', return_value='user'):
                call_command('team', '-create', 'management')

    def test_delete_team_without_permission(self):
        with self.assertRaises(CommandError):
            with patch('builtins.input', return_value='user'):
                call_command('team', '-delete', 'sales')

    def test_read_team_without_permission(self):
        with self.assertRaises(CommandError):
            with patch('builtins.input', return_value='user'):
                call_command('team', '-read', 'sales')