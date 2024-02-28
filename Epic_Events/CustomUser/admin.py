from django.contrib import admin
from .models import CustomUserAccount, CustomToken

class CustomUserAccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'team', 'is_admin')

class CustomTokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'created', 'expires_at')

admin.site.register(CustomUserAccount, CustomUserAccountAdmin)
admin.site.register(CustomToken, CustomTokenAdmin)