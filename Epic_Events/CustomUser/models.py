from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin, Permission
from django.utils import timezone
from rest_framework.authtoken.models import Token


class TeamManagement(models.Manager):
    def create_team(self, team_name, permissions):
        team, created = self.get_or_create(name=team_name)
        if created:
            for perm_codename in permissions:
                try:
                    perm = Permission.objects.get(codename=perm_codename)
                    team.permissions.add(perm)
                except Permission.DoesNotExist:
                    print(f'Permission "{perm_codename}" does not exist.')
        return team

    def create_management_team(self):
        permissions = ['create_user', 'update_user', 'delete_user', 'create_contract', 'update_all_contracts', 'update_all_events']
        return self.create_team('management', permissions)

    def create_sales_team(self):
        permissions = ['create_client', 'update_client', 'update_contract', 'create_event']
        return self.create_team('sales', permissions)

    def create_support_team(self):
        permissions = ['update_event']
        return self.create_team('support', permissions)

class Team(models.Model):
    name = models.CharField(max_length=50, unique=True)
    permissions = models.ManyToManyField(Permission)

    objects = TeamManagement()

    def __str__(self):
        return self.name


class CustomUserAccountManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, email, phone_number, password, team_name=None):
        try:
            with transaction.atomic(): 
                for field in self.model.REQUIRED_FIELDS:
                    if field not in kwargs or not kwargs[field]:
                        raise ValueError(f"The {field} field is required.")

                email = self.normalize_email(email)

                user = self.model(username=username, email=email,
                                first_name=first_name, last_name=last_name,
                                phone_number=phone_number, team=team)

                user.set_password(password)

                if team_name:
                    team_creation_method = getattr(Team.objects, f'create_{team_name}_team', None)
                    if not team_creation_method:
                        raise ValueError(f'Invalid team name: {team_name}')
                    team = team_creation_method()
                    user.team = team

                user.save()

                return user

        except InterruptedError:
            raise ValueError("There was a problem creating the user. Please ensure the username and email are unique.")
        except Exception as e:
            raise ValueError(f"Unexpected error occurred while creating user: {str(e)}")


    def create_superuser(self, username, email, first_name, last_name, phone, password):

        user = self.create_user(username=username, email=email, first_name=first_name,
                                last_name=last_name, phone=phone, password=password)

        user.is_staff = True
        user.is_superuser = True

        user.save()

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return user


class CustomUserAccount(AbstractUser, PermissionsMixin):

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'users'
        default_permissions = ()
        permissions = (
            ('view_user', 'Can view user'),
            ('add_user', 'Can add user'),
            ('change_user', 'Can change user'),
            ('delete_user', 'Can delete user'),
        )

    ## Fields Already defined in AbstractUser :
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)

    username = models.CharField(max_length=50, unique=True, blank=False, null=False)
    email = models.EmailField(max_length=150, unique=True, blank=False, null=False)
    # password = models.CharField(max_length=128)

    # last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    # is_superuser = models.BooleanField(default=False)
    # is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    ## Fields Not defined in AbstractUser :
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name='users')
    phone_number = models.CharField(max_length=50)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'password', 'phone', 'team']

    def __str__(self) -> str:
        """returns user contact info"""
        return f"username: {self.username}, email: {self.email}, phone: {self.phone}"


class CustomToken(Token):
    expires_at = models.DateTimeField()
    
    def refresh(self):
        self.expires_at = timezone.now() + timezone.timedelta(hours=1)
        self.save()
        return self

    def save(self, *args, **kwargs):
        self.expires_at = timezone.now() + timezone.timedelta(hours=1)
        super().save(*args, **kwargs)