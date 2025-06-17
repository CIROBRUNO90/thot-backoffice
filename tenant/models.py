from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import get_user_model

User = get_user_model()


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


class BusinessUnitUser(models.Model):
    """
    Modelo intermedio para manejar la relación muchos a muchos entre usuarios
    y unidades de negocio
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Usuario'),
        related_name='business_unit_assignments'
    )
    business_unit = models.ForeignKey(
        BusinessUnit,
        on_delete=models.CASCADE,
        verbose_name=_('Unidad de Negocio'),
        related_name='user_assignments'
    )
    is_primary = models.BooleanField(
        _('Unidad Principal'),
        default=False,
        help_text=_(
            'Indica si esta es la unidad de negocio principal del usuario'
        )
    )
    created_at = models.DateTimeField(
        _('Fecha de creación'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _('Fecha de actualización'),
        auto_now=True
    )

    class Meta:
        verbose_name = _('Usuario y Unidad de Negocio')
        verbose_name_plural = _(
            'Usuarios y Unidades de Negocio'
        )
        unique_together = ['user', 'business_unit']
        ordering = ['user', '-is_primary', 'business_unit__name']

    def __str__(self):
        return f"{self.user.username} - {self.business_unit.name}"

    def save(self, *args, **kwargs):
        # Si esta es la unidad principal, desactivar otras unidades principales del usuario
        if self.is_primary:
            BusinessUnitUser.objects.filter(
                user=self.user,
                is_primary=True
            ).exclude(
                id=self.id
            ).update(is_primary=False)
        super().save(*args, **kwargs)
