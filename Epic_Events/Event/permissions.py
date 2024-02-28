from Event.models import Event
from CustomUser.models import CustomUserAccount


class IsSupport:
    def __init__(self, user: CustomUserAccount):
        self.user = user
    
    def has_permission(self):
        # Check if the user is a manager
        return self.user.team.name == "support"


class IsEventContact:
    def __init__(self, user: CustomUserAccount, event: Event):
        self.user = user
        self.event = event

    def has_permission(self):
        # Check if the user is a manager
        return self.user == self.event.contact_support_EE