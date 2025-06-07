# admin.py
from django.contrib import admin
from django.utils.html import format_html

from .models import Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = [
        'business_name',
        'tax_id',
        'contact_info_display',  # Método personalizado para mostrar información de contacto
        'location_display',      # Método personalizado para mostrar ubicación
        'status_display',        # Método personalizado para mostrar estado
        'created_at'
    ]

    fieldsets = (
        ('Información Principal', {
            'fields': (
                'business_name',
                'commercial_name',
                'tax_id',
                'is_active'
            )
        }),
        ('Información de Contacto', {
            'fields': (
                'contact_person',
                'email',
                'phone'
            )
        }),
        ('Ubicación', {
            'fields': (
                'address',
                'city',
                'country'
            )
        }),
        ('Información Bancaria', {
            'fields': (
                'bank_name',
                'bank_cbu_alias'
            ),
            'classes': ('collapse',),  # Esta sección será colapsable
            'description': 'Información confidencial para pagos'
        }),
        ('Información Adicional', {
            'fields': (
                'notes',
            ),
            'classes': ('collapse',)
        })
    )

    # Configuramos los campos por los que se puede buscar
    search_fields = [
        'business_name',
        'commercial_name',
        'tax_id',
        'contact_person',
        'email'
    ]

    # Configuramos los filtros que aparecerán en la barra lateral
    list_filter = [
        'is_active',
        'country',
        'city',
        'created_at'
    ]

    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20

    def contact_info_display(self, obj):
        """
        Muestra la información de contacto de manera organizada y visual
        """
        return format_html(
            '<div style="line-height: 1.5;">'
            '<strong>{}</strong><br>'
            '<a href="mailto:{}">{}</a><br>'
            '<span>{}</span>'
            '</div>',
            obj.contact_person,
            obj.email,
            obj.email,
            obj.phone
        )
    contact_info_display.short_description = 'Información de Contacto'

    def location_display(self, obj):
        """
        Muestra la ubicación de manera concisa
        """
        return format_html(
            '{}, <strong>{}</strong>',
            obj.city,
            obj.country
        )
    location_display.short_description = 'Ubicación'

    def status_display(self, obj):
        """
        Muestra el estado del proveedor con un indicador visual
        """
        return format_html(
            '<span style="background-color: {}; padding: 3px 10px; border-radius: 3px; color: white;">{}</span>',
            '#28a745' if obj.is_active else '#dc3545',
            'Activo' if obj.is_active else 'Inactivo'
        )
    status_display.short_description = 'Estado'

    def save_model(self, request, obj, form, change):
        """
        Sobrescribimos el método save_model para realizar acciones adicionales
        al guardar un proveedor
        """
        # Convertimos el nombre de la empresa a mayúsculas para mantener consistencia
        obj.business_name = obj.business_name.upper()
        if obj.commercial_name:
            obj.commercial_name = obj.commercial_name.upper()

        super().save_model(request, obj, form, change)

    class Media:
        """
        Agregamos archivos CSS y JavaScript personalizados para mejorar la interfaz
        """
        css = {
            'all': ('admin/css/supplier_admin.css',)
        }
        js = ('admin/js/supplier_admin.js',)
