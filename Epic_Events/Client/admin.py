from django.contrib import admin
from .models import Client

class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'company_name', 'creation_date', 'contact_sales_EE')

admin.site.register(Client, ClientAdmin)