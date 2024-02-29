# Python
from django.core.management import call_command
from django.test import TestCase
from CustomUser.models import CustomUserAccount, Team, CustomToken
from django.core.management import call_command
from django.core.management.base import CommandError
from unittest.mock import patch
from Epic_Events.utils import refresh_or_create_token, verify_token

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