from django.db import models
from django.utils.translation import gettext_lazy as _


class Customer(models.Model):
    name = models.CharField(_('Nombre'), max_length=255)
    email = models.EmailField(_('Email'), unique=True)
    phone = models.CharField(_('Teléfono'), max_length=20, blank=True)
    address = models.TextField(_('Dirección'), blank=True)
    created_at = models.DateTimeField(
        _('Fecha de creación'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _('Fecha de actualización'),
        auto_now=True
    )

    class Meta:
        verbose_name = _('Empresa')
        verbose_name_plural = _('Empresas')
        ordering = ['name']

    def __str__(self):
        return self.name


class BusinessUnit(models.Model):
    customer = models.ForeignKey(
        Customer,
        verbose_name=_('Cliente'),
        on_delete=models.CASCADE,
        related_name='business_units'
    )
    name = models.CharField(_('Nombre de la unidad'), max_length=255)
    description = models.TextField(_('Descripción'), blank=True)
    is_active = models.BooleanField(_('Activa'), default=True)
    created_at = models.DateTimeField(
        _('Fecha de creación'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _('Fecha de actualización'),
        auto_now=True
    )

    class Meta:
        verbose_name = _('Unidad de Negocio')
        verbose_name_plural = _('Unidades de Negocio')
        ordering = ['customer', 'name']
        unique_together = ['customer', 'name']

    def __str__(self):
        return f"{self.customer.name} - {self.name}"
