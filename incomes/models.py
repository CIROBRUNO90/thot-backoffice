from django.db import models
from django.utils.translation import gettext_lazy as _

from .constants import (
    OrderStatus, PaymentStatus, ShippingStatus, PaymentMethod,
    ShippingMethod, BusinessType, Currency
)
from tenant.models import BusinessUnit


class Income(models.Model):
    """
    Modelo para almacenar los ingresos (ventas) de diferentes tipos de negocios
    """
    # Relación con unidad de negocio
    business_unit = models.ForeignKey(
        BusinessUnit,
        on_delete=models.PROTECT,
        verbose_name=_('Unidad de Negocio'),
        help_text=_('Unidad de negocio a la que pertenece la venta'),
        related_name='incomes',
        null=True,
        blank=True
    )
    # Información básica de la venta
    order_number = models.CharField(
        _('Número de orden/venta/factura'),
        max_length=30
    )
    date = models.DateField(_('Fecha'))
    business_type = models.CharField(
        _('Tipo de negocio'),
        max_length=20,
        choices=BusinessType.choices,
        default=BusinessType.PHYSICAL
    )
    order_status = models.CharField(
        _('Estado de la orden'),
        max_length=30,
        choices=OrderStatus.choices,
        default=OrderStatus.OPEN
    )
    payment_status = models.CharField(
        _('Estado del pago'),
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )
    currency = models.CharField(
        _('Moneda'),
        max_length=3,
        choices=Currency.choices,
        default=Currency.ARS
    )

    # Información financiera
    product_subtotal = models.DecimalField(
        _('Subtotal de productos'),
        max_digits=12,
        decimal_places=2,
        default=0
    )
    discount = models.DecimalField(
        _('Descuento'),
        max_digits=12,
        decimal_places=2,
        default=0
    )
    shipping_cost = models.DecimalField(
        _('Costo de envío'),
        max_digits=12,
        decimal_places=2,
        default=0
    )
    total = models.DecimalField(
        _('Total'),
        max_digits=12,
        decimal_places=2,
        default=0,
        editable=True
    )

    # Información del cliente
    buyer_name = models.CharField(
        _('Nombre del cliente'),
        max_length=255,
        blank=True,
        null=True
    )
    email = models.EmailField(
        _('Email'),
        max_length=255,
        blank=True,
        null=True
    )
    tax_id = models.CharField(
        _('DNI / CUIT'),
        max_length=20,
        blank=True,
        null=True
    )
    phone = models.CharField(
        _('Teléfono'),
        max_length=20,
        blank=True,
        null=True
    )

    # Información de envío (opcional)
    shipping_status = models.CharField(
        _('Estado del envío'),
        max_length=20,
        choices=ShippingStatus.choices,
        default=ShippingStatus.NOT_REQUIRED,
        blank=True,
        null=True
    )
    shipping_method = models.CharField(
        _('Medio de envío'),
        max_length=20,
        choices=ShippingMethod.choices,
        default=ShippingMethod.NOT_REQUIRED,
        blank=True,
        null=True
    )
    shipping_name = models.CharField(
        _('Nombre para el envío'),
        max_length=255,
        blank=True,
        null=True
    )
    shipping_phone = models.CharField(
        _('Teléfono para el envío'),
        max_length=20,
        blank=True,
        null=True
    )
    address = models.CharField(
        _('Dirección'),
        max_length=255,
        blank=True,
        null=True
    )
    address_number = models.CharField(
        _('Número'),
        max_length=20,
        blank=True,
        null=True
    )
    floor_apt = models.CharField(
        _('Piso'),
        max_length=50,
        blank=True,
        null=True
    )
    locality = models.CharField(
        _('Localidad'),
        max_length=100,
        blank=True,
        null=True
    )
    city = models.CharField(
        _('Ciudad'),
        max_length=100,
        blank=True,
        null=True
    )
    postal_code = models.CharField(
        _('Código postal'),
        max_length=20,
        blank=True,
        null=True
    )
    state_province = models.CharField(
        _('Provincia o estado'),
        max_length=100,
        blank=True,
        null=True
    )
    country = models.CharField(
        _('País'),
        max_length=100,
        blank=True,
        null=True
    )

    # Información de pago
    payment_method = models.CharField(
        _('Medio de pago'),
        max_length=20,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CASH
    )
    payment_date = models.DateField(
        _('Fecha de pago'),
        blank=True,
        null=True
    )
    payment_transaction_id = models.CharField(
        _('ID de transacción'),
        max_length=255,
        blank=True,
        null=True
    )
    discount_coupon = models.CharField(
        _('Cupón de descuento'),
        max_length=100,
        blank=True,
        null=True
    )

    # Información del producto
    product_name = models.CharField(
        _('Nombre del producto'),
        max_length=255,
        blank=True,
        null=True
    )
    product_price = models.DecimalField(
        _('Precio del producto'),
        max_digits=12,
        decimal_places=2,
        default=0
    )
    product_quantity = models.PositiveIntegerField(
        _('Cantidad del producto'),
        default=1
    )
    sku = models.CharField(
        _('SKU'),
        max_length=50,
        blank=True,
        null=True
    )
    is_physical_product = models.BooleanField(
        _('Producto Físico'),
        default=True
    )

    # Información adicional
    channel = models.CharField(
        _('Canal de venta'),
        max_length=50,
        blank=True,
        null=True
    )
    tracking_code = models.CharField(
        _('Código de tracking'),
        max_length=100,
        blank=True,
        null=True
    )

    # Información de personal
    registered_by = models.CharField(
        _('Registrado por'),
        max_length=100,
        blank=True,
        null=True
    )
    sales_branch = models.CharField(
        _('Sucursal'),
        max_length=100,
        blank=True,
        null=True
    )
    seller = models.CharField(
        _('Vendedor'),
        max_length=100,
        blank=True,
        null=True
    )

    # Notas
    buyer_notes = models.TextField(
        _('Notas del cliente'),
        blank=True,
        null=True
    )
    seller_notes = models.TextField(
        _('Notas del vendedor'),
        blank=True,
        null=True
    )

    # Metadatos
    created_at = models.DateTimeField(
        _('Fecha de creación'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _('Fecha de actualización'),
        auto_now=True
    )

    class Meta:
        verbose_name = _('Ingreso')
        verbose_name_plural = _('Ingresos')
        ordering = ['-date']
        indexes = [
            models.Index(fields=['order_number']),
            models.Index(fields=['date']),
            models.Index(fields=['order_status']),
            models.Index(fields=['payment_status']),
            models.Index(fields=['business_type']),
            models.Index(fields=['business_unit']),
            models.Index(fields=['buyer_name']),
            models.Index(fields=['id']),
        ]

    def __str__(self):
        business_unit_name = self.business_unit.name if self.business_unit else 'Sin unidad'
        return (f"{business_unit_name} - {self.get_business_type_display()} - "
                f"#{self.order_number} - {self.buyer_name or 'Sin cliente'} - "
                f"{self.total} {self.currency}")

    def save(self, *args, **kwargs):
        from decimal import Decimal

        product_subtotal = self.product_subtotal or Decimal('0')
        discount = self.discount or Decimal('0')
        shipping_cost = self.shipping_cost or Decimal('0')

        discount = min(discount, product_subtotal)

        self.total = product_subtotal - discount + shipping_cost
        self.total = max(self.total, Decimal('0'))

        super().save(*args, **kwargs)
