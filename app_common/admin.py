from django.contrib import admin
from . import models
# Register your models here.

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ("full_name","contact")
    list_display = ("full_name", "contact", "wallet", "is_active", "is_superuser", "is_staff")
