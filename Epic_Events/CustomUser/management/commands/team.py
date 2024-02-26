# Python
from django.core.management.base import BaseCommand, CommandError
from CustomUser.models import Team, CustomUserAccount

class Command(BaseCommand):
    help = 'Manage teams'

    def add_arguments(self, parser):
        parser.add_argument('-list', action='store_true', help='List all teams')
        parser.add_argument('-create', action='store_true', help='Create a new team')
        parser.add_argument('-delete', action='store_true', help='Delete a team')
        parser.add_argument('-read', action='store_true', help='Read a team details')
        parser.add_argument('team_name', nargs='?', type=str)

    def handle(self, *args, **options):
        if options['list']:
            self.list_teams()
        elif options['create']:
            self.create_team(options)
        elif options['delete']:
            self.delete_team(options)
        elif options['read']:
            self.read_team(options)
        else:
            raise CommandError('Invalid command')

    def list_teams(self):
        for team in Team.objects.all():
            self.stdout.write(str(team))

    def create_team(self, options):
        team_name = options['team_name'] or input('Enter team name: ')
        try:
            team_creation_method = getattr(Team.objects, f'create_{team_name}_team', None)
            if not team_creation_method:
                raise ValueError(f'Invalid team name: {team_name}')
            team = team_creation_method()
            self.stdout.write(f'Successfully created team {team}')
        except Exception as e:
            raise CommandError(str(e))

    def delete_team(self, options):
        team_name = options['team_name'] or input('Enter name of team to delete: ')
        try:
            team = Team.objects.get(name=team_name)
            team.delete()
            self.stdout.write(f'Successfully deleted team {team_name}')
        except Team.DoesNotExist:
            raise CommandError('Team does not exist')

    def read_team(self, options):
        team_name = options['team_name'] or input('Enter name of team to read: ')
        try:
            team = Team.objects.get(name=team_name)
            self.stdout.write(str(team))
        except Team.DoesNotExist:
            raise CommandError('Team does not exist')