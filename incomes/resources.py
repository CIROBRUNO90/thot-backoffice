from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, DateWidget

from .models import Income
from tenant.models import BusinessUnit


class IncomeResource(resources.ModelResource):
    business_unit = fields.Field(
        column_name='Unidad Negocio',
        attribute='business_unit',
        widget=ForeignKeyWidget(BusinessUnit, 'name')
    )

    business_type = fields.Field(
        column_name='Tipo Negocio',
        attribute='business_type'
    )

    date = fields.Field(
        column_name='Fecha',
        attribute='date',
        widget=DateWidget(format='%d/%m/%Y')
    )

    order_number = fields.Field(
        column_name='Número de Orden',
        attribute='order_number'
    )

    buyer_name = fields.Field(
        column_name='Nombre del Comprador',
        attribute='buyer_name'
    )

    total = fields.Field(
        column_name='Total',
        attribute='total'
    )

    currency = fields.Field(
        column_name='Moneda',
        attribute='currency'
    )

    payment_status = fields.Field(
        column_name='Estado de Pago',
        attribute='payment_status'
    )

    order_status = fields.Field(
        column_name='Estado de Orden',
        attribute='order_status'
    )

    shipping_status = fields.Field(
        column_name='Estado de Envío',
        attribute='shipping_status'
    )

    payment_method = fields.Field(
        column_name='Método de Pago',
        attribute='payment_method'
    )

    product_name = fields.Field(
        column_name='Producto',
        attribute='product_name'
    )

    product_price = fields.Field(
        column_name='Precio Producto',
        attribute='product_price'
    )

    product_quantity = fields.Field(
        column_name='Cantidad',
        attribute='product_quantity'
    )

    product_subtotal = fields.Field(
        column_name='Subtotal',
        attribute='product_subtotal'
    )

    discount = fields.Field(
        column_name='Descuento',
        attribute='discount'
    )

    shipping_cost = fields.Field(
        column_name='Costo de Envío',
        attribute='shipping_cost'
    )

    discount_coupon = fields.Field(
        column_name='Cupón de Descuento',
        attribute='discount_coupon'
    )

    email = fields.Field(
        column_name='Email',
        attribute='email'
    )

    tax_id = fields.Field(
        column_name='CUIT/DNI',
        attribute='tax_id'
    )

    phone = fields.Field(
        column_name='Teléfono',
        attribute='phone'
    )

    shipping_name = fields.Field(
        column_name='Nombre de Envío',
        attribute='shipping_name'
    )

    shipping_phone = fields.Field(
        column_name='Teléfono de Envío',
        attribute='shipping_phone'
    )

    address = fields.Field(
        column_name='Dirección',
        attribute='address'
    )

    address_number = fields.Field(
        column_name='Número',
        attribute='address_number'
    )

    floor_apt = fields.Field(
        column_name='Piso/Depto',
        attribute='floor_apt'
    )

    locality = fields.Field(
        column_name='Localidad',
        attribute='locality'
    )

    city = fields.Field(
        column_name='Ciudad',
        attribute='city'
    )

    postal_code = fields.Field(
        column_name='Código Postal',
        attribute='postal_code'
    )

    state_province = fields.Field(
        column_name='Provincia',
        attribute='state_province'
    )

    country = fields.Field(
        column_name='País',
        attribute='country'
    )

    tracking_code = fields.Field(
        column_name='Código de Seguimiento',
        attribute='tracking_code'
    )

    payment_transaction_id = fields.Field(
        column_name='ID Transacción',
        attribute='payment_transaction_id'
    )

    payment_date = fields.Field(
        column_name='Fecha de Pago',
        attribute='payment_date',
        widget=DateWidget(format='%d/%m/%Y')
    )

    buyer_notes = fields.Field(
        column_name='Notas del Comprador',
        attribute='buyer_notes'
    )

    seller_notes = fields.Field(
        column_name='Notas del Vendedor',
        attribute='seller_notes'
    )

    created_at = fields.Field(
        column_name='Fecha Creación',
        attribute='created_at'
    )

    class Meta:
        model = Income
        fields = (
            'id', 'date', 'business_unit', 'business_type', 'order_number',
            'buyer_name', 'total', 'currency', 'payment_status', 'order_status',
            'shipping_status', 'payment_method', 'product_name', 'product_price',
            'product_quantity', 'product_subtotal', 'discount', 'shipping_cost',
            'discount_coupon', 'email', 'tax_id', 'phone', 'shipping_name',
            'shipping_phone', 'address', 'address_number', 'floor_apt',
            'locality', 'city', 'postal_code', 'state_province', 'country',
            'tracking_code', 'payment_transaction_id', 'payment_date',
            'buyer_notes', 'seller_notes', 'created_at'
        )
        export_order = (
            'id', 'date', 'business_unit', 'business_type', 'order_number',
            'buyer_name', 'total', 'currency', 'payment_status', 'order_status',
            'shipping_status', 'payment_method', 'product_name', 'product_price',
            'product_quantity', 'product_subtotal', 'discount', 'shipping_cost',
            'discount_coupon', 'email', 'tax_id', 'phone', 'shipping_name',
            'shipping_phone', 'address', 'address_number', 'floor_apt',
            'locality', 'city', 'postal_code', 'state_province', 'country',
            'tracking_code', 'payment_transaction_id', 'payment_date',
            'buyer_notes', 'seller_notes', 'created_at'
        )
        import_id_fields = ['id']
