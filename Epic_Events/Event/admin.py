from django.contrib import admin
from .models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'contract', 'client', 'contact_support_EE', 'date_start', 'date_end', 'location', 'attendees', 'notes')

admin.site.register(Event, EventAdmin)