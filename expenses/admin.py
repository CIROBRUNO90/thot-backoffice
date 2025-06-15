import logging
from datetime import datetime

from django.contrib import admin
from django.db.models import Sum
from django.utils.html import format_html
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.db.models.functions import TruncMonth
from import_export.formats import base_formats

from rangefilter.filters import DateRangeFilter

from .models import Expenses, ExpenseType
from .resources import ExpensesResource

logger = logging.getLogger(__name__)


@admin.register(ExpenseType)
class ExpenseTypeAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']
    search_fields = ['code', 'name']
    ordering = ['name']


@admin.register(Expenses)
class ExpensesAdmin(admin.ModelAdmin):
    list_display = [
        'date',
        'business_unit_display',
        'expense_type_display',
        'amount_display',
        'is_fixed'
    ]

    list_filter = [
        ('date', DateRangeFilter),
        'business_unit',
        'business_unit__customer',
        'expense_type',
        'is_fixed'
    ]

    search_fields = [
        'expense_type__name',
        'expense_type__code',
        'business_unit__name',
        'business_unit__customer__name'
    ]

    fieldsets = (
        ('Información Principal', {
            'fields': (
                'date',
                'business_unit',
                'expense_type',
                'amount',
                'is_fixed'
            )
        }),
        ('Detalles Adicionales', {
            'fields': ('observations',),
            'classes': ('collapse',)
        })
    )

    def export_selected_to_csv(modeladmin, request, queryset):
        """
        Exporta los registros seleccionados a CSV usando el mismo formato que Excel
        """
        resource = ExpensesResource()
        dataset = resource.export(queryset)
        csv_format = base_formats.CSV()
        response = HttpResponse(
            csv_format.export_data(dataset),
            content_type=csv_format.get_content_type()
        )
        response['Content-Disposition'] = (
            f'attachment; filename=expenses-'
            f'{datetime.now().strftime("%Y%m%d")}.csv'
        )

        return response

    def export_selected_to_excel(modeladmin, request, queryset):
        """
        Exporta los registros seleccionados a Excel usando django-import-export
        """
        resource = ExpensesResource()
        dataset = resource.export(queryset)
        xlsx_format = base_formats.XLSX()
        response = HttpResponse(
            xlsx_format.export_data(dataset),
            content_type=xlsx_format.get_content_type()
        )
        response['Content-Disposition'] = (
            f'attachment; filename=expenses-'
            f'{datetime.now().strftime("%Y%m%d")}.xlsx'
        )
        return response

    export_selected_to_csv.short_description = "Exportar seleccionados a CSV"
    export_selected_to_excel.short_description = "Exportar seleccionados a Excel"

    def get_queryset(self, request):
        """
        Optimización de consultas y filtrado por unidad de negocio del usuario
        """
        queryset = super().get_queryset(request)

        # Si el usuario es superusuario, mostrar todos los registros
        if request.user.is_superuser:
            return queryset.select_related('business_unit', 'expense_type')

        # Usar el filtro de unidad de negocio del middleware
        return queryset.filter(
            request.business_unit_filter
        ).select_related('business_unit', 'expense_type')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # Si el usuario no es superusuario, filtrar las unidades de negocio disponibles
        if not request.user.is_superuser:
            form.base_fields['business_unit'].queryset = form.base_fields['business_unit'].queryset.filter(
                id__in=request.user_business_units
            )
            # Si el usuario solo tiene una unidad de negocio, preseleccionar esa unidad
            if len(request.user_business_units) == 1:
                form.base_fields['business_unit'].initial = request.user_business_units[0]
                form.base_fields['business_unit'].widget.attrs['disabled'] = True

        return form

    def business_unit_display(self, obj):
        """
        Muestra la unidad de negocio con formato especial
        """
        return format_html(
            '<div class="business-unit-container">'
            '<span style="background-color: #4A90E2; color: white; padding: 4px 12px; '
            'border-radius: 4px; display: inline-block; min-width: 100px; '
            'text-align: center; font-weight: 500;">{}</span>'
            '</div>',
            obj.business_unit.name if obj.business_unit else 'Sin unidad'
        )
    business_unit_display.short_description = 'Unidad de Negocio'

    def expense_type_display(self, obj):
        """
        Mejora la visualización del tipo de gasto con un código de colores,
        generando colores dinámicamente basados en el código del tipo de gasto.
        """
        def generate_color_from_code(code):
            """
            Genera un color único basado en el código del tipo de gasto.
            Usa una función hash simple para generar un color consistente.
            """
            # Usamos el código como semilla para generar un color consistente
            hash_value = sum(ord(c) for c in code)

            # Generamos componentes RGB usando el hash
            r = (hash_value * 17) % 256
            g = (hash_value * 31) % 256
            b = (hash_value * 13) % 256

            # Aseguramos que el color no sea demasiado oscuro
            r = max(r, 100)
            g = max(g, 100)
            b = max(b, 100)

            return f'#{r:02x}{g:02x}{b:02x}'

        def get_text_color(bg_color):
            """
            Determina si el texto debe ser negro o blanco basado en el color de fondo.
            Utiliza la fórmula de luminosidad relativa (percepción humana de brillo).
            """
            bg_color = bg_color.lstrip('#')
            r = int(bg_color[0:2], 16)
            g = int(bg_color[2:4], 16)
            b = int(bg_color[4:6], 16)

            # Calcula la luminosidad usando la fórmula de luminosidad relativa
            luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255

            # Si la luminosidad es mayor a 0.5, el fondo es claro y necesitamos texto oscuro
            return '#000000' if luminance > 0.5 else '#FFFFFF'

        if not obj.expense_type:
            return format_html(
                '<div class="expense-type-container">'
                '<span style="background-color: #E6E6E6; color: #000000; padding: 4px 12px; '
                'border-radius: 4px; display: inline-block; min-width: 100px; '
                'text-align: center; font-weight: 500;">Sin tipo</span>'
                '</div>'
            )

        bg_color = generate_color_from_code(obj.expense_type.code)
        text_color = get_text_color(bg_color)

        return format_html(
            '<div class="expense-type-container">'
            '<span style="background-color: {}; color: {}; padding: 4px 12px; '
            'border-radius: 4px; display: inline-block; min-width: 100px; '
            'text-align: center; font-weight: 500;">{}</span>'
            '</div>',
            bg_color,
            text_color,
            obj.expense_type.name
        )
    expense_type_display.short_description = 'Tipo de Gasto'

    def amount_display(self, obj):
        """
        Formatea el monto con color según su valor y alineación correcta.
        Si el tipo de gasto tiene un límite definido,
        muestra en rojo cuando se excede.
        Si no hay límite definido, muestra en verde.
        """
        formatted_amount = "${:,.2f}".format(float(obj.amount))

        # Verifica si existe un tipo de gasto y si tiene límite definido
        if obj.expense_type and obj.expense_type.limit is not None:
            color = 'red' if obj.amount > obj.expense_type.limit else 'green'
        else:
            color = 'green'

        return format_html(
            '<div class="amount-cell" style="color:{};">{}</div>',
            color,
            formatted_amount
        )
    amount_display.short_description = 'Monto'

    def changelist_view(self, request, extra_context=None):
        """
        Añade estadísticas al pie de la lista de gastos
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
                    """
                    Formatea el monto con separadores de miles y dos decimales
                    """
                    return f"${amount:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

                totales = {
                    'total': format_amount(
                        queryset.aggregate(total=Sum('amount'))['total'] or 0
                    ),
                    'por_mes': [
                        {
                            'mes': mes['mes'],
                            'total': format_amount(mes['total'])
                        }
                        for mes in queryset.annotate(
                            mes=TruncMonth('date')
                        ).values('mes').annotate(
                            total=Sum('amount')
                        ).order_by('-mes')[:3]
                    ],
                    'por_categoria': [
                        {
                            'nombre': cat['expense_type__name'],
                            'total': format_amount(cat['total'])
                        }
                        for cat in queryset.values(
                            'expense_type__name'
                        ).annotate(
                            total=Sum('amount')
                        ).order_by('-total')
                    ],
                    'por_unidad': [
                        {
                            'nombre': unit['business_unit__name'] if unit['business_unit__name'] else 'Sin unidad',
                            'total': format_amount(unit['total'])
                        }
                        for unit in queryset.values(
                            'business_unit__name'
                        ).annotate(
                            total=Sum('amount')
                        ).order_by('-total')
                    ]
                }

                response.context_data['totales'] = totales

            except Exception as e:
                logger.error(f"Error en changelist_view: {str(e)}")
                response.context_data['totales'] = {
                    'total': format_amount(0),
                    'por_mes': [],
                    'por_categoria': [],
                    'por_unidad': []
                }

        return response

    actions = [export_selected_to_csv, export_selected_to_excel]
    ordering = ['-date']
    list_per_page = 20
