from django.db import models
from django.utils.translation import gettext_lazy as _


class OrderStatus(models.TextChoices):
    OPEN = 'abierta', _('Abierta')
    CLOSED = 'cerrada', _('Cerrada')
    CANCELLED = 'cancelada', _('Cancelada')
    # Añadir otros estados según sea necesario


class PaymentStatus(models.TextChoices):
    PENDING = 'pendiente', _('Pendiente')
    PAID = 'pagado', _('Pagado')
    CANCELLED = 'cancelado', _('Cancelado')
    # Añadir otros estados según sea necesario


class ShippingStatus(models.TextChoices):
    NOT_PACKAGED = 'no_empaquetado', _('No está empaquetado')
    PACKAGED = 'empaquetado', _('Empaquetado')
    SHIPPED = 'enviado', _('Enviado')
    DELIVERED = 'entregado', _('Entregado')
    # Añadir otros estados según sea necesario
