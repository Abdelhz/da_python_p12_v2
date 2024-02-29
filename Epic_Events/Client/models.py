from django.db import models
from CustomUser.models import CustomUserAccount
from phonenumber_field.modelfields import PhoneNumberField


class ClientManager(models.Manager):
    def create_client(self, full_name, email, phone_number, company_name, contact_sales_EE, information):
        
        client = self.create(
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            company_name=company_name,
            contact_sales_EE=contact_sales_EE,
            information=information
        )
        return client

    def update_client(self, client, **kwargs):
        for attr, value in kwargs.items():
            setattr(client, attr, value)
        client.save()
        return client


class Client(models.Model):
    full_name = models.CharField(max_length=150, blank=False, null=False)
    email = models.EmailField(max_length=50, blank=False, null=False)
    phone_number = PhoneNumberField(blank=False, null=False)
    company_name = models.CharField(max_length=150, blank=False, null=False, unique=True)
    creation_date = models.DateField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    contact_sales_EE = models.ForeignKey(CustomUserAccount, on_delete=models.SET_NULL, null=True)
    information = models.TextField()
    
    objects = ClientManager()

    REQUIRED_FIELDS = ['full_name', 'email', 'phone_number', 'company_name']

    def __str__(self):
        return (
            f"Client name: {self.full_name}\n"
            f"Email: {self.email}\n"
            f"Phone number: {self.phone_number}\n"
            f"Company name : {self.company_name}\n"
            f"Epic Events contact name: username : {self.contact_sales_EE.username}, First name : {self.contact_sales_EE.first_name}, Last name : {self.contact_sales_EE.last_name}\n"
            f"Client information : {self.information}\n"
            f"Creation date : {self.creation_date}\n"
            f"Last update : {self.last_update}\n"
        )