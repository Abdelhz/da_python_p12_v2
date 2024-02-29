from CustomUser.models import CustomUserAccount, CustomToken
from Epic_Events.utils import verify_token
from pathlib import Path
import json

KEY_FILE = Path.home() / 'my_app_key.json'

class IsAuthenticated:
    def __init__(self, user: CustomUserAccount):
        self.user = user
        try:
            self.token = CustomToken.objects.get(user=user)
        except CustomToken.DoesNotExist:
            self.token = None

    def has_permission(self):
        # Check if the token exists, belongs to the user, the user is active, and the token is valid
        return self.token is not None and self.token.user == self.user and self.user.is_active and verify_token(self.token)


class IsSuperuser:
    def __init__(self, user: CustomUserAccount):
        self.user = user

    def has_permission(self):
        # Check if the user is a superuser
        return self.user.is_superuser

class IsManager:
    def __init__(self, user: CustomUserAccount):
        self.user = user

    def has_permission(self):
        # Check if the user is a manager
        return self.user.team.name == "management"


class IsSameUser:
    def __init__(self, user: CustomUserAccount, current_user: CustomUserAccount):
        self.user = user
        self.current_user = current_user

    def has_permission(self):
        # Check if the user is the same as the other user
        return self.user == self.current_user