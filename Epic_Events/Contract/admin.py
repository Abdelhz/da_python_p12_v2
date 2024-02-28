from django.contrib import admin
from .models import Contract

class ContractAdmin(admin.ModelAdmin):
    list_display = ('unique_id', 'client', 'contact_sales_EE', 'total_amount', 'remaining_amount', 'creation_date', 'signature_status')

admin.site.register(Contract, ContractAdmin)