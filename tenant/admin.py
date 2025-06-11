from django.contrib import admin
from .models import Customer, BusinessUnit


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('created_at',)
    ordering = ('name',)

@admin.register(BusinessUnit)
class BusinessUnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'customer', 'is_active', 'created_at')
    list_filter = ('is_active', 'customer', 'created_at')
    search_fields = ('name', 'customer__name', 'description')
    ordering = ('customer', 'name')
