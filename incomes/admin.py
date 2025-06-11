from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum
from django.template.response import TemplateResponse

from .models import Income


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = (
        'business_unit_display',  # Unidad de negocio al inicio
        'order_number',
        'buyer_name',
        'date',
        'total_display',
        'order_status',
        'payment_status',
        'shipping_status'
    )
    list_filter = (
        'business_unit__customer',  # Filtro por cliente
        'business_unit',  # Filtro por unidad de negocio
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
        'payment_transaction_id',
        'business_unit__name',  # Búsqueda por nombre de unidad
        'business_unit__customer__name'  # Búsqueda por nombre de cliente
    )
    date_hierarchy = 'date'
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20

    fieldsets = (
        ('Información de la Orden', {
            'fields': (
                'business_unit',  # Unidad de negocio al inicio
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

    def business_unit_display(self, obj):
        """Mostrar la unidad de negocio con formato especial"""
        return format_html(
            '<div style="line-height: 1.5;">'
            '<span style="color: #666;">{}</span><br>'
            '<strong style="color: #2c3e50;">{}</strong>'
            '</div>',
            obj.business_unit.customer.name,
            obj.business_unit.name
        )
    business_unit_display.short_description = 'Unidad de Negocio'

    def total_display(self, obj):
        """Mostrar el total con formato de moneda"""
        return format_html(
            '<span style="color: {}; font-weight: bold">{} {}</span>',
            '#28a745',  # Color verde para las ventas
            obj.total,
            obj.currency
        )
    total_display.short_description = 'Total'

    def changelist_view(self, request, extra_context=None):
        """
        Añade estadísticas al pie de la lista de ingresos
        """
        response = super().changelist_view(request, extra_context=extra_context)

        if isinstance(response, TemplateResponse):
            try:
                if 'cl' in response.context_data:
                    queryset = response.context_data['cl'].queryset
                else:
                    queryset = self.model.objects.all()

                if hasattr(response.context_data.get('cl', None), 'get_queryset'):
                    queryset = response.context_data['cl'].get_queryset(request)

                def format_amount(amount):
                    """Formatea el monto con separadores de miles y dos decimales"""
                    return f"${amount:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

                totales = {
                    'total': format_amount(
                        queryset.aggregate(total=Sum('total'))['total'] or 0
                    ),
                    'por_unidad': [
                        {
                            'nombre': unit['business_unit__name'],
                            'total': format_amount(unit['total'])
                        }
                        for unit in queryset.values(
                            'business_unit__name'
                        ).annotate(
                            total=Sum('total')
                        ).order_by('-total')
                    ],
                    'por_cliente': [
                        {
                            'nombre': client['business_unit__customer__name'],
                            'total': format_amount(client['total'])
                        }
                        for client in queryset.values(
                            'business_unit__customer__name'
                        ).annotate(
                            total=Sum('total')
                        ).order_by('-total')
                    ]
                }

                response.context_data['totales'] = totales

            except Exception as e:
                response.context_data['totales'] = {
                    'total': format_amount(0),
                    'por_unidad': [],
                    'por_cliente': []
                }

        return response

    def get_queryset(self, request):
        """Optimización de consultas para mejorar el rendimiento"""
        queryset = super().get_queryset(request)
        return queryset.select_related(
            'business_unit', 
            'business_unit__customer'
        )
