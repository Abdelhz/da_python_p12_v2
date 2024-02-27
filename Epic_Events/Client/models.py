from django.db import models
from CustomUser.models import CustomUserAccount
from phonenumber_field.modelfields import PhoneNumberField


class ClientManager(models.Manager):
    def create_client(self, full_name, email, phone_number, company_name, address, contact_sales_EE, information):
        unique_id = self.generate_unique_id()
        client = self.create(
            unique_id=unique_id,
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            company_name=company_name,
            address=address,
            contact_sales_EE=contact_sales_EE,
            information=information
        )
        return client

    def update_client(self, client, **kwargs):
        for attr, value in kwargs.items():
            setattr(client, attr, value)
        client.save()
        return client
    
    def generate_unique_id(self):
        unique_id = self.format_unique_id(str(random.randint(10**14, 10**15 - 1)))
        while self.filter(unique_id=unique_id).exists():
            unique_id = self.format_unique_id(str(random.randint(10**14, 10**15 - 1)))
        return unique_id

    def format_unique_id(self, unique_id):
        return '-'.join([unique_id[i:i+4] for i in range(0, len(unique_id), 4)])


class Client(models.Model):
    full_name = models.CharField(max_length=150, blank=False, null=False)
    email = models.EmailField(max_length=50, blank=False, null=False)
    phone_number = PhoneNumberField(blank=False, null=False)
    company_name = models.CharField(max_length=150, blank=False, null=False, unique=True)
    unique_id = models.CharField(max_length=50, blank=False, null=False, unique=True)
    creation_date = models.DateField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    contact_sales_EE = models.ForeignKey(CustomUserAccount, on_delete=models.SET_NULL, null=True)
    information = models.TextField()
    
    objects = ClientManager()

    REQUIRED_FIELDS = ['full_name', 'email', 'phone_number', 'company_name']

    def __str__(self):
        return (
            f"Client name: {self.name}\nemail: {self.email}\n"
            f" phone: {self.phone}\nclient contact name: {self.client_contact_name}\n"
            f"Epic Events contact name: {self.contact_sales_EE.first_name} {self.contact_sales_EE.last_name}\n"
        )