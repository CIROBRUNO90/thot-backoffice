from django.db import models
from django.utils.translation import gettext_lazy as _

from .constants import OrderStatus, PaymentStatus, ShippingStatus


class Income(models.Model):
    """
    Modelo para almacenar los ingresos (ventas) del e-commerce
    Basado en la estructura del archivo CSV de ventas proporcionado
    """
    # Información de la orden
    order_number = models.CharField(_('Número de orden'), max_length=30)
    email = models.EmailField(_('Email'), max_length=255)
    date = models.DateField(_('Fecha'))
    order_status = models.CharField(
        _('Estado de la orden'),
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.OPEN
    )
    payment_status = models.CharField(
        _('Estado del pago'),
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )
    shipping_status = models.CharField(
        _('Estado del envío'),
        max_length=20,
        choices=ShippingStatus.choices,
        default=ShippingStatus.NOT_PACKAGED
    )
    currency = models.CharField(_('Moneda'), max_length=3)

    # Información financiera
    product_subtotal = models.DecimalField(
        _('Subtotal de productos'),
        max_digits=12,
        decimal_places=2
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
    total = models.DecimalField(_('Total'), max_digits=12, decimal_places=2)

    # Información del comprador
    buyer_name = models.CharField(_('Nombre del comprador'), max_length=255)
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

    # Información de envío
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
    city = models.CharField(_('Ciudad'), max_length=100, blank=True, null=True)
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

    # Métodos de pago y envío
    shipping_method = models.CharField(
        _('Medio de envío'),
        max_length=255,
        blank=True,
        null=True
    )
    payment_method = models.CharField(
        _('Medio de pago'),
        max_length=100,
        blank=True,
        null=True
    )
    discount_coupon = models.CharField(
        _('Cupón de descuento'),
        max_length=100,
        blank=True,
        null=True
    )

    # Notas
    buyer_notes = models.TextField(
        _('Notas del comprador'),
        blank=True,
        null=True
    )
    seller_notes = models.TextField(
        _('Notas del vendedor'),
        blank=True,
        null=True
    )

    # Fechas adicionales
    payment_date = models.DateField(_('Fecha de pago'), blank=True, null=True)
    shipping_date = models.DateField(
        _('Fecha de envío'),
        blank=True,
        null=True
    )

    # Información del producto
    product_name = models.CharField(_('Nombre del producto'), max_length=255)
    product_price = models.DecimalField(
        _('Precio del producto'),
        max_digits=12,
        decimal_places=2
    )
    product_quantity = models.PositiveIntegerField(_('Cantidad del producto'))
    sku = models.CharField(_('SKU'), max_length=50, blank=True, null=True)

    # Información adicional
    channel = models.CharField(
        _('Canal'),
        max_length=50,
        blank=True,
        null=True
    )
    tracking_code = models.CharField(
        _('Código de tracking del envío'),
        max_length=100,
        blank=True,
        null=True
    )
    payment_transaction_id = models.CharField(
        _('Identificador de la transacción en el medio de pago'),
        max_length=255,
        blank=True,
        null=True
    )
    order_id = models.CharField(
        _('Identificador de la orden'),
        max_length=50,
        unique=True
    )
    is_physical_product = models.BooleanField(
        _('Producto Físico'),
        default=True
    )

    # Información de personal
    registered_by = models.CharField(
        _('Persona que registró la venta'),
        max_length=100,
        blank=True,
        null=True
    )
    sales_branch = models.CharField(
        _('Sucursal de venta'),
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
            models.Index(fields=['email']),
            models.Index(fields=['date']),
            models.Index(fields=['order_status']),
            models.Index(fields=['payment_status']),
            models.Index(fields=['shipping_status']),
            models.Index(fields=['buyer_name']),
            models.Index(fields=['order_id']),
        ]

    def __str__(self):
        return f"Orden #{self.order_number} - {self.buyer_name} - {self.total} {self.currency}"

    def save(self, *args, **kwargs):
        # Asegurarse de que el total se calcule correctamente
        if self.product_subtotal and self.discount is not None and self.shipping_cost is not None:
            self.total = self.product_subtotal - self.discount + self.shipping_cost
        super().save(*args, **kwargs)
