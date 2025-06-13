from django.db import models
from django.utils.translation import gettext_lazy as _


class OrderStatus(models.TextChoices):
    OPEN = 'abierta', _('Abierta')
    PENDING = 'pendiente', _('Pendiente')
    PROCESSING = 'procesando', _('Procesando')
    COMPLETED = 'completada', _('Completada')
    CANCELLED = 'cancelada', _('Cancelada')
    REFUNDED = 'reembolsada', _('Reembolsada')
    ON_HOLD = 'en_espera', _('En espera')
    PARTIALLY_REFUNDED = 'parcialmente_reembolsada', _('Parcialmente reembolsada')


class PaymentStatus(models.TextChoices):
    PENDING = 'pendiente', _('Pendiente')
    PAID = 'pagado', _('Pagado')
    PARTIALLY_PAID = 'parcialmente_pagado', _('Parcialmente pagado')
    REFUNDED = 'reembolsado', _('Reembolsado')
    FAILED = 'fallido', _('Fallido')
    CANCELLED = 'cancelado', _('Cancelado')


class ShippingStatus(models.TextChoices):
    NOT_PACKAGED = 'no_empaquetado', _('No empaquetado')
    PACKAGED = 'empaquetado', _('Empaquetado')
    SHIPPED = 'enviado', _('Enviado')
    DELIVERED = 'entregado', _('Entregado')
    RETURNED = 'devuelto', _('Devuelto')
    NOT_REQUIRED = 'no_requiere', _('No requiere envío')


class PaymentMethod(models.TextChoices):
    CASH = 'efectivo', _('Efectivo')
    CREDIT_CARD = 'tarjeta_credito', _('Tarjeta de crédito')
    DEBIT_CARD = 'tarjeta_debito', _('Tarjeta de débito')
    BANK_TRANSFER = 'transferencia', _('Transferencia bancaria')
    MERCADO_PAGO = 'mercado_pago', _('Mercado Pago')
    PAYPAL = 'paypal', _('PayPal')
    OTHER = 'otro', _('Otro')


class ShippingMethod(models.TextChoices):
    PICKUP = 'retiro', _('Retiro en local')
    DELIVERY = 'envio', _('Envío a domicilio')
    EXPRESS = 'express', _('Envío express')
    STANDARD = 'estandar', _('Envío estándar')
    NOT_REQUIRED = 'no_requiere', _('No requiere envío')


class BusinessType(models.TextChoices):
    ECOMMERCE = 'ecommerce', _('E-commerce')
    PHYSICAL = 'fisico', _('Local físico')
    MIXED = 'mixto', _('Mixto')


class Currency(models.TextChoices):
    ARS = 'ARS', _('Peso Argentino')
    USD = 'USD', _('Dólar Estadounidense')
    EUR = 'EUR', _('Euro')
    BRL = 'BRL', _('Real Brasileño')
    CLP = 'CLP', _('Peso Chileno')
    UYU = 'UYU', _('Peso Uruguayo')
    PEN = 'PEN', _('Sol Peruano')
    COP = 'COP', _('Peso Colombiano')
    MXN = 'MXN', _('Peso Mexicano')