import logging

from django.contrib import admin
from django.db.models import Sum
from django.utils.html import format_html
from django.template.response import TemplateResponse
from django.db.models.functions import TruncMonth

from rangefilter.filters import DateRangeFilter

from .models import Expenses, ExpenseType

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
        'expense_type_display',
        'amount_display',
        'observations',
        'is_fixed'
    ]

    list_filter = [
        ('date', DateRangeFilter),
        'expense_type',
        'is_fixed'
    ]

    search_fields = [
        'observations',
        'expense_type__name',
        'expense_type__code'
    ]

    fieldsets = (
        ('Información Principal', {
            'fields': ('date', 'expense_type', 'amount', 'is_fixed')
        }),
        ('Detalles Adicionales', {
            'fields': ('observations',),
            'classes': ('collapse',)
        })
    )

    ordering = ['-date']
    list_per_page = 20

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
        Formatea el monto con color según su valor y alineación correcta
        """
        formatted_amount = "${:,.2f}".format(float(obj.amount))
        return format_html(
            '<div class="amount-cell" style="color:{};">{}</div>',
            'red' if obj.amount > 700000 else 'green',
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
                    ]
                }

                response.context_data['totales'] = totales

            except Exception as e:
                logger.error(f"Error en changelist_view: {str(e)}")
                response.context_data['totales'] = {
                    'total': format_amount(0),
                    'por_mes': [],
                    'por_categoria': []
                }

        return response

    class Media:
        """
        Añadimos estilos personalizados para mejorar la visualización
        """
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
