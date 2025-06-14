import logging
from datetime import datetime

from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum
from django.template.response import TemplateResponse
from django.db.models.functions import TruncMonth
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django import forms
from import_export.formats import base_formats

from rangefilter.filters import DateRangeFilter

from .models import Income
from .resources import IncomeResource


logger = logging.getLogger(__name__)


class IncomeAdminForm(forms.ModelForm):
    """Formulario personalizado para validar que el total no sea 0"""
    # Campo calculado de solo lectura
    calculated_total = forms.DecimalField(
        label='Total Calculado',
        required=False,
        widget=forms.TextInput(attrs={
            'readonly': 'readonly',
            'style': 'background-color: #f0f0f0; font-weight: bold;'
        }),
        help_text='Este valor se calcula automáticamente: Subtotal - Descuento + Envío'
    )
    
    class Meta:
        model = Income
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si hay datos, calcular el total
        if self.instance and self.instance.pk:
            subtotal = self.instance.product_subtotal or 0
            discount = self.instance.discount or 0
            shipping = self.instance.shipping_cost or 0
            self.fields['calculated_total'].initial = subtotal - discount + shipping

    def clean(self):
        cleaned_data = super().clean()

        # Obtener valores
        product_subtotal = cleaned_data.get('product_subtotal', 0) or 0
        discount = cleaned_data.get('discount', 0) or 0
        shipping_cost = cleaned_data.get('shipping_cost', 0) or 0

        # Calcular total
        calculated_total = product_subtotal - discount + shipping_cost

        # Validar que el total sea mayor que 0
        if calculated_total <= 0:
            raise ValidationError({
                'product_subtotal': f'El total calculado ({calculated_total}) debe ser mayor que 0. Ajuste el subtotal, descuento o costo de envío.'
            })

        # Asignar el total calculado
        cleaned_data['total'] = calculated_total

        return cleaned_data


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    form = IncomeAdminForm
    list_display = (
        'id',
        'business_unit_display',
        'business_type_display',
        'order_number',
        'date',
        'total_display',
        'payment_status',
    )
    list_filter = (
        'business_type',
        'business_unit__customer',
        'business_unit',
        ('date', DateRangeFilter),
        'order_status',
        'payment_status',
        'payment_method',
    )
    search_fields = (
        'id',
        'order_number',
        'email',
        'product_name',
        'tax_id',
        'payment_transaction_id',
        'business_unit__name',
        'business_unit__customer__name'
    )

    def export_selected_to_csv(modeladmin, request, queryset):
        """
        Exporta los registros seleccionados a CSV usando el mismo formato que Excel
        """
        resource = IncomeResource()
        dataset = resource.export(queryset)
        csv_format = base_formats.CSV()
        response = HttpResponse(
            csv_format.export_data(dataset),
            content_type=csv_format.get_content_type()
        )
        response['Content-Disposition'] = (
            f'attachment; filename=incomes-'
            f'{datetime.now().strftime("%Y%m%d")}.csv'
        )
        return response

    def export_selected_to_excel(modeladmin, request, queryset):
        """
        Exporta los registros seleccionados a Excel usando django-import-export
        """
        resource = IncomeResource()
        dataset = resource.export(queryset)
        xlsx_format = base_formats.XLSX()
        response = HttpResponse(
            xlsx_format.export_data(dataset),
            content_type=xlsx_format.get_content_type()
        )
        response['Content-Disposition'] = (
            f'attachment; filename=incomes-'
            f'{datetime.now().strftime("%Y%m%d")}.xlsx'
        )
        return response

    export_selected_to_csv.short_description = "Exportar seleccionados a CSV"
    export_selected_to_excel.short_description = "Exportar seleccionados a Excel"

    fieldsets = (
        ('Información Principal', {
            'fields': (
                'id_display',
                'business_unit',
                'business_type',
                'order_number',
                'date',
                'order_status',
                'payment_status',
                'currency'
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
        ('Información del Cliente', {
            'fields': (
                'buyer_name',
                'email',
                'tax_id',
                'phone'
            )
        }),
        ('Información de Pago', {
            'fields': (
                'payment_method',
                'payment_transaction_id',
                'payment_date'
            )
        }),
        ('Información Financiera', {
            'fields': (
                'product_subtotal',
                'discount',
                'shipping_cost',
                'total',
                'discount_coupon'
            ),
            'description': 'El total se calcula automáticamente: Subtotal - Descuento + Envío'
        }),
        ('Información de Envío', {
            'fields': (
                'shipping_status',
                'shipping_method',
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
                'tracking_code'
            ),
            'classes': ('collapse',)
        }),
        ('Notas', {
            'fields': (
                'buyer_notes',
                'seller_notes'
            ),
            'classes': ('collapse',)
        }),
        ('Metadatos', {
            'fields': (
                'channel',
                'registered_by',
                'sales_branch',
                'seller',
                'created_at',
                'updated_at'
            ),
            'classes': ('collapse',)
        })
    )

    def id_display(self, obj):
        """Mostrar el ID del objeto o el próximo ID si es nuevo"""
        if obj.id:
            return obj.id
        else:
            try:
                last_income = Income.objects.order_by('-id').first()
                next_id = (last_income.id + 1) if last_income else 1
                return f"{next_id} (próximo)"
            except Exception:
                return "Nuevo"
    id_display.short_description = 'ID'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if 'total' in form.base_fields:
            form.base_fields['total'].widget.attrs.update({
                'readonly': 'readonly',
                'style': 'background-color: #f8f9fa;'
            })

        return form

    def get_fields(self, request, obj=None):
        fields = list(super().get_fields(request, obj))
        if 'total' not in fields:
            fields.append('total')
        return fields

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)

        for fieldset in fieldsets:
            if fieldset[0] == 'Información Financiera':
                fields = list(fieldset[1]['fields'])
                # Mover 'total' al final si existe
                if 'total' in fields:
                    fields.remove('total')
                fields.append('total')
                fieldset[1]['fields'] = tuple(fields)

        return fieldsets

    def business_unit_display(self, obj):
        """Mostrar la unidad de negocio con formato especial"""
        if not obj.business_unit:
            return format_html(
                '<div style="line-height: 1.5;">'
                '<span style="color: #666;">Sin cliente</span><br>'
                '<strong style="color: #2c3e50;">Sin unidad</strong>'
                '</div>'
            )
        return format_html(
            '<div style="line-height: 1.5;">'
            '<span style="color: #666;">{}</span><br>'
            '<strong style="color: #2c3e50;">{}</strong>'
            '</div>',
            obj.business_unit.customer.name,
            obj.business_unit.name
        )
    business_unit_display.short_description = 'Unidad de Negocio'

    def business_type_display(self, obj):
        """Mostrar el tipo de negocio con formato especial"""
        colors = {
            'ecommerce': '#4A90E2',  # Azul
            'physical': '#2ECC71',   # Verde
            'mixed': '#F1C40F'       # Amarillo
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; '
            'border-radius: 4px; display: inline-block; min-width: 100px; '
            'text-align: center; font-weight: 500;">{}</span>',
            colors.get(obj.business_type, '#95A5A6'),
            obj.get_business_type_display()
        )
    business_type_display.short_description = 'Tipo de Negocio'

    def shipping_status_display(self, obj):
        """Mostrar el estado de envío con formato especial"""
        if not obj.shipping_status:
            return format_html(
                '<span style="color: #95A5A6;">No requiere envío</span>'
            )
        colors = {
            'not_packaged': '#E74C3C',  # Rojo
            'packaged': '#F39C12',      # Naranja
            'shipped': '#3498DB',       # Azul
            'delivered': '#2ECC71',     # Verde
            'returned': '#E74C3C',      # Rojo
            'not_required': '#95A5A6'   # Gris
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; '
            'border-radius: 4px; display: inline-block; min-width: 100px; '
            'text-align: center; font-weight: 500;">{}</span>',
            colors.get(obj.shipping_status, '#95A5A6'),
            obj.get_shipping_status_display()
        )
    shipping_status_display.short_description = 'Estado de Envío'

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
                    'por_tipo': [
                        {
                            'nombre': tipo['business_type'],
                            'total': format_amount(tipo['total'])
                        }
                        for tipo in queryset.values(
                            'business_type'
                        ).annotate(
                            total=Sum('total')
                        ).order_by('-total')
                    ],
                    'por_mes': [
                        {
                            'mes': mes['mes'],
                            'total': format_amount(mes['total'])
                        }
                        for mes in queryset.annotate(
                            mes=TruncMonth('date')
                        ).values('mes').annotate(
                            total=Sum('total')
                        ).order_by('-mes')[:3]
                    ],
                    'por_unidad': [
                        {
                            'nombre': unit['business_unit__name'] or 'Sin unidad',
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
                            'nombre': client['business_unit__customer__name'] or 'Sin cliente',
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
                    'por_tipo': [],
                    'por_mes': [],
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

    date_hierarchy = 'date'
    readonly_fields = ('id_display', 'created_at', 'updated_at')
    list_per_page = 20
    actions = [
        export_selected_to_csv,
        export_selected_to_excel
    ]

    class Media:
        js = ('js/income_calculator.js',)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        return readonly_fields
