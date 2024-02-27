from Client.models import Client
from CustomUser.models import CustomUserAccount


class IsSales:
    def __init__(self, user: CustomUserAccount):
        self.user = user
    
    def has_permission(self):
        # Check if the user is a manager
        return self.user.team.name == "sales"


class IsClientContact:
    def __init__(self, user: CustomUserAccount, client: Client):
        self.user = user
        self.client = client

    def has_permission(self):
        # Check if the user is a manager
        return self.user == self.client.contact_sales_EE