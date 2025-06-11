from django.db import models
from django.utils.translation import gettext_lazy as _

from thot.models import TimestampsMixin
from tenant.models import BusinessUnit


class Supplier(TimestampsMixin):

    business_unit = models.ForeignKey(
        BusinessUnit,
        on_delete=models.PROTECT,
        verbose_name=_('Unidad de Negocio'),
        help_text=_('Unidad de negocio a la que pertenece el proveedor'),
        related_name='suppliers',
        null=True,
        blank=True
    )

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
        help_text=_('Nombre completo de la persona de contacto principal'),
        null=True,
        blank=True
    )

    email = models.EmailField(
        verbose_name=_('Correo Electrónico'),
        help_text=_('Correo electrónico principal del proveedor'),
        null=True,
        blank=True
    )

    phone = models.CharField(
        max_length=20,
        verbose_name=_('Teléfono'),
        help_text=_('Número de teléfono principal del proveedor'),
        null=True,
        blank=True
    )

    address = models.TextField(
        verbose_name=_('Dirección'),
        help_text=_('Dirección completa del proveedor'),
        null=True,
        blank=True
    )

    city = models.CharField(
        max_length=100,
        verbose_name=_('Ciudad'),
        null=True,
        blank=True
    )

    country = models.CharField(
        max_length=100,
        verbose_name=_('País'),
        null=True,
        blank=True
    )

    bank_name = models.CharField(
        max_length=100,
        verbose_name=_('Banco'),
        blank=True,
        help_text=_('Nombre del banco para transferencias'),
        null=True,
    )

    bank_cbu_alias = models.CharField(
        max_length=100,
        verbose_name=_('CBU/ALIAS'),
        blank=True,
        help_text=_('CBU o ALIAS bancario para transferencias'),
        null=True,
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Activo'),
        help_text=_('Indica si el proveedor está activo en el sistema')
    )

    notes = models.TextField(
        blank=True,
        verbose_name=_('Notas'),
        help_text=_('Notas adicionales sobre el proveedor'),
        null=True,
    )

    class Meta:
        verbose_name = _('Proveedor')
        verbose_name_plural = _('Proveedores')
        ordering = ['business_name']
        indexes = [
            models.Index(fields=['business_name']),
            models.Index(fields=['tax_id']),
            models.Index(fields=['business_unit']),
        ]

    def __str__(self):
        return f"{self.business_unit.name} - {self.business_name} ({self.tax_id})"

    def get_full_address(self):
        """
        Método que retorna la dirección completa formateada
        """
        if self.address and self.city and self.country:
            return f"{self.address}, {self.city}, {self.country}"
        elif self.address:
            return self.address
        elif self.city:
            return self.city
        elif self.country:
            return self.country
        else:
            return ""
