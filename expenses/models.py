from django.db import models
from django.utils.translation import gettext_lazy as _

from thot.models import TimestampsMixin
from tenant.models import BusinessUnit


class ExpenseType(TimestampsMixin):
    code = models.CharField(
        max_length=3,
        unique=True,
        verbose_name=_('Código'),
        help_text=_('Código único para el tipo de gasto')
    )

    name = models.CharField(
        max_length=50,
        verbose_name=_('Nombre'),
        help_text=_('Nombre del tipo de gasto')
    )

    limit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Límite'),
        help_text=_('Límite máximo permitido para este tipo de gasto'),
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('Tipo de Gasto')
        verbose_name_plural = _('Tipos de Gastos')
        ordering = ['name']

    def __str__(self):
        return self.name


class Expenses(TimestampsMixin):
    date = models.DateField(
        verbose_name=_('Fecha del gasto'),
        help_text=_('Fecha en que se realizó el gasto')
    )

    business_unit = models.ForeignKey(
        BusinessUnit,
        on_delete=models.PROTECT,
        verbose_name=_('Unidad de Negocio'),
        help_text=_('Unidad de negocio a la que pertenece el gasto'),
        related_name='expenses',
        null=True,
        blank=True
    )

    expense_type = models.ForeignKey(
        ExpenseType,
        on_delete=models.PROTECT,
        verbose_name=_('Tipo de gasto'),
        help_text=_('Categoría o tipo de gasto realizado'),
        null=True,
        blank=True
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Monto'),
        help_text=_('Monto total del gasto')
    )

    is_fixed = models.BooleanField(
        null=True,
        verbose_name=_('Gasto fijo'),
        help_text=_('Indica si el gasto es fijo o variable')
    )

    observations = models.TextField(
        blank=True,
        verbose_name=_('Observaciones'),
        help_text=_('Observaciones o notas adicionales sobre el gasto')
    )

    class Meta:
        verbose_name = _('Gasto')
        verbose_name_plural = _('Gastos')
        ordering = ['-date']

    def __str__(self):
        if self.business_unit and self.expense_type:
            return f"{self.business_unit.name} - {self.expense_type.name} - {self.date} - ${self.amount}"
        elif self.business_unit:
            return f"{self.business_unit.name} - Sin tipo - {self.date} - ${self.amount}"
        elif self.expense_type:
            return f"Sin unidad - {self.expense_type.name} - {self.date} - ${self.amount}"
        else:
            return f"Sin unidad - Sin tipo - {self.date} - ${self.amount}"
