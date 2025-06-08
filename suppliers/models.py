from django.db import models
from django.utils.translation import gettext_lazy as _

from thot.models import TimestampsMixin


class Supplier(TimestampsMixin):

    business_name = models.CharField(
        max_length=200,
        verbose_name=_('Razón Social'),
        help_text=_('Nombre legal de la empresa proveedora')
    )

    commercial_name = models.CharField(
        max_length=200,
        verbose_name=_('Nombre Comercial'),
        blank=True,
        help_text=_('Nombre comercial o de fantasía del proveedor')
    )

    tax_id = models.CharField(
        max_length=20,
        unique=True,
        verbose_name=_('Identificación Fiscal'),
        help_text=_('Número de identificación fiscal (DNI, CUIT, CUIL, etc.)')
    )

    contact_person = models.CharField(
        max_length=100,
        verbose_name=_('Persona de Contacto'),
        help_text=_('Nombre completo de la persona de contacto principal')
    )

    email = models.EmailField(
        verbose_name=_('Correo Electrónico'),
        help_text=_('Correo electrónico principal del proveedor')
    )

    phone = models.CharField(
        max_length=20,
        verbose_name=_('Teléfono'),
        help_text=_('Número de teléfono principal del proveedor')
    )

    address = models.TextField(
        verbose_name=_('Dirección'),
        help_text=_('Dirección completa del proveedor')
    )

    city = models.CharField(
        max_length=100,
        verbose_name=_('Ciudad')
    )

    country = models.CharField(
        max_length=100,
        verbose_name=_('País')
    )

    bank_name = models.CharField(
        max_length=100,
        verbose_name=_('Banco'),
        blank=True,
        help_text=_('Nombre del banco para transferencias')
    )

    bank_cbu_alias = models.CharField(
        max_length=100,
        verbose_name=_('CBU/ALIAS'),
        blank=True,
        help_text=_('CBU o ALIAS bancario para transferencias')
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Activo'),
        help_text=_('Indica si el proveedor está activo en el sistema')
    )

    notes = models.TextField(
        blank=True,
        verbose_name=_('Notas'),
        help_text=_('Notas adicionales sobre el proveedor')
    )

    class Meta:
        verbose_name = _('Proveedor')
        verbose_name_plural = _('Proveedores')
        ordering = ['business_name']
        indexes = [
            models.Index(fields=['business_name']),
            models.Index(fields=['tax_id']),
        ]

    def __str__(self):
        return f"{self.business_name} ({self.tax_id})"

    def get_full_address(self):
        """
        Método que retorna la dirección completa formateada
        """
        return f"{self.address}, {self.city}, {self.country}"
