from django.db import models
from Client.models import Client
from CustomUser.models import CustomUserAccount
from Contract.models import Contract

class EventManager(models.Manager):

    def create_event(self, event_name, contract, contact_support_EE, date_start, date_end, location, attendees, notes):
        event = self.create(
            event_name=event_name,
            contract=contract,
            client=contract.client,
            contact_support_EE=contact_support_EE,
            date_start=date_start,
            date_end=date_end,
            location=location,
            attendees=attendees,
            notes=notes,
        )
        return contract

    def update_event(self, event, **kwargs):
        for attr, value in kwargs.items():
            setattr(event, attr, value)
        event.save()
        return event

class Event(models.Model):
    event_name = models.CharField(max_length=100, blank=False, null=False)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=False, blank=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=False, blank=False)
    contact_support_EE = models.ForeignKey(CustomUserAccount, on_delete=models.SET_NULL, null=True, default=None)
    date_start = models.DateTimeField(null=True, blank=True)
    date_end = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    attendees = models.IntegerField(null=True, blank=True)
    notes = models.TextField(max_length=2000, null=True, blank=True)




    objects = EventManager()

    def __str__(self):
        return (
            f"Event name: {self.event_name}\n"
            f"Contract ID: {self.contract.unique_id}\n"
            f"Client: {self.client.full_name}, Company name: {self.client.company_name}\n"
            f"Client email: {self.client.email}, Client phone number: {self.client.phone_number}\n"
            f"Start date: {self.date_start}\nEnd date: {self.date_end}\n"
            f"Contact: {self.contact_support_EE.first_name} {self.contact_support_EE.last_name}\n"
            f"Attendees: {self.attendees}\n"
            f"Status: {'Signed' if self.status else 'Not Signed'}\n"
            f"Notes: {self.notes}"
                        
        )