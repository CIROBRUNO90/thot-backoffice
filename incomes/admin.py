from django.contrib import admin
from django.utils.html import format_html

from .models import Income


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = (
        'order_number',
        'buyer_name',
        'date',
        'total_display',
        'order_status',
        'payment_status',
        'shipping_status'
    )
    list_filter = (
        'order_status',
        'payment_status',
        'shipping_status',
        'date',
        'currency',
        'country',
        'payment_method',
        'shipping_method',
        'channel'
    )
    search_fields = (
        'order_number',
        'buyer_name',
        'email',
        'product_name',
        'tax_id',
        'order_id',
        'payment_transaction_id'
    )
    date_hierarchy = 'date'
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Información de la Orden', {
            'fields': (
                'order_number', 'order_id', 'email', 'date', 'order_status', 
                'payment_status', 'shipping_status', 'currency'
            )
        }),
        ('Información Financiera', {
            'fields': (
                'product_subtotal',
                'discount',
                'shipping_cost',
                'total',
                'discount_coupon'
            )
        }),
        ('Información del Comprador', {
            'fields': (
                'buyer_name', 'tax_id', 'phone'
            )
        }),
        ('Información de Envío', {
            'fields': (
                'shipping_name',
                'shipping_phone',
                'address',
                'address_number',
                'floor_apt',
                'locality',
                'city',
                'postal_code',
                'state_province',
                'country',
                'shipping_method',
                'tracking_code'
            )
        }),
        ('Información del Producto', {
            'fields': (
                'product_name',
                'product_price',
                'product_quantity',
                'sku',
                'is_physical_product'
            )
        }),
        ('Información de Pago', {
            'fields': (
                'payment_method', 'payment_transaction_id', 'payment_date'
            )
        }),
        ('Notas', {
            'fields': (
                'buyer_notes', 'seller_notes'
            )
        }),
        ('Información Adicional', {
            'fields': (
                'channel',
                'shipping_date',
                'registered_by',
                'sales_branch',
                'seller',
                'created_at',
                'updated_at'
            )
        })
    )

    def total_display(self, obj):
        """Mostrar el total con formato de moneda"""
        return format_html(
            '<span style="color: {}; font-weight: bold">{} {}</span>',
            '#28a745',  # Color verde para las ventas
            obj.total,
            obj.currency
        )
    total_display.short_description = 'Total'

    def get_queryset(self, request):
        """Optimización de consultas para mejorar el rendimiento"""
        queryset = super().get_queryset(request)
        return queryset.select_related()
