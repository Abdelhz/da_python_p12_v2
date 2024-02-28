from django.db import models
from Client.models import Client
from CustomUser.models import CustomUserAccount
import random

class ContractManager(models.Manager):
    def generate_unique_id(self):
        unique_id = self.format_unique_id(str(random.randint(10**14, 10**15 - 1)))
        while self.filter(unique_id=unique_id).exists():
            unique_id = self.format_unique_id(str(random.randint(10**14, 10**15 - 1)))
        return unique_id

    def format_unique_id(self, unique_id):
        return '-'.join([unique_id[i:i+4] for i in range(0, len(unique_id), 4)])

    def create_contract(self, client, total_amount, remaining_amount, signature_status):
        unique_id = self.generate_unique_id()
        contract = self.create(
            unique_id=unique_id,
            client=client,
            contact_sales_EE=client.contact_sales_EE,
            total_amount=total_amount,
            remaining_amount=remaining_amount,
            signature_status=signature_status
        )
        return contract

    def update_contract(self, contract, **kwargs):
        for attr, value in kwargs.items():
            setattr(contract, attr, value)
        contract.save()
        return contract

class Contract(models.Model):
    unique_id = models.CharField(max_length=50, blank=False, null=False, unique=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    contact_sales_EE = models.ForeignKey(CustomUserAccount, on_delete=models.SET_NULL, null=True)
    total_amount = models.FloatField(blank=False, null=False)
    remaining_amount = models.FloatField(blank=False, null=False)
    creation_date = models.DateField(auto_now_add=True)
    signature_status = models.BooleanField(default=False)

    objects = ContractManager()

    def __str__(self):
        return (
            f"Contract ID: {self.unique_id}\n"
            f"Client: {self.client.full_name}, Company name: {self.client.company_name}\n"
            f"Client email: {self.client.email}, Client phone number: {self.client.phone_number}\n"
            f"Contact: {self.contact_sales_EE.first_name} {self.contact_sales_EE.last_name}\n"
            f"Total Amount: {self.total_amount}\nRemaining Amount: {self.remaining_amount}\n"
            f"Creation Date: {self.creation_date}\nStatus: {'Signed' if self.status else 'Not Signed'}"
        )