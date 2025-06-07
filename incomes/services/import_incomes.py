import csv
import datetime
import os
import django
from decimal import Decimal

from django.utils.dateparse import parse_date

from incomes.models import Income

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()


def clean_decimal(value):
    """Convierte un valor a decimal, manejando formatos y valores nulos"""
    if not value or value == '':
        return Decimal('0')
    # Eliminar posibles símbolos de moneda y espacios
    value = str(value).replace('$', '').replace(' ', '').replace(',', '.')
    try:
        return Decimal(value)
    except:
        return Decimal('0')


def parse_date_string(date_string):
    """
    Convierte una cadena de fecha a un objeto date, manejando varios formatos
    """
    if not date_string or date_string == '':
        return None

    try:
        # Formato dd/mm/yyyy
        if '/' in date_string:
            day, month, year = date_string.split('/')
            return datetime.date(int(year), int(month), int(day))
        # Formato yyyy-mm-dd
        elif '-' in date_string:
            return parse_date(date_string)
        return None
    except:
        return None


def import_csv(file_path):
    """Importa datos de un archivo CSV al modelo Income"""
    count = 0
    errors = 0

    print(f"Iniciando importación desde {file_path}")

    with open(file_path, 'r', encoding='cp1252') as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            try:
                # Manejar valores booleanos
                is_physical = True
                if 'Producto Físico' in row and row['Producto Físico'].lower() in ['no', 'n', 'false', '0']:
                    is_physical = False

                # Crear instancia del modelo
                income = Income(
                    # Información de la orden
                    order_number=row.get('Número de orden', ''),
                    email=row.get('Email', ''),
                    date=parse_date_string(row.get('Fecha')),
                    order_status=row.get('Estado de la orden', 'abierta'),
                    payment_status=row.get('Estado del pago', 'pendiente'),
                    shipping_status=row.get('Estado del envío', 'no_empaquetado'),
                    currency=row.get('Moneda', 'ARS'),

                    # Información financiera
                    product_subtotal=clean_decimal(row.get('Subtotal de productos')),
                    discount=clean_decimal(row.get('Descuento')),
                    shipping_cost=clean_decimal(row.get('Costo de envío')),
                    total=clean_decimal(row.get('Total')),

                    # Información del comprador
                    buyer_name=row.get('Nombre del comprador', ''),
                    tax_id=row.get('DNI / CUIT', ''),
                    phone=row.get('Teléfono', ''),

                    # Información de envío
                    shipping_name=row.get('Nombre para el envío', ''),
                    shipping_phone=row.get('Teléfono para el envío', ''),
                    address=row.get('Dirección', ''),
                    address_number=row.get('Número', ''),
                    floor_apt=row.get('Piso', ''),
                    locality=row.get('Localidad', ''),
                    city=row.get('Ciudad', ''),
                    postal_code=row.get('Código postal', ''),
                    state_province=row.get('Provincia o estado', ''),
                    country=row.get('País', ''),

                    # Métodos de pago y envío
                    shipping_method=row.get('Medio de envío', ''),
                    payment_method=row.get('Medio de pago', ''),
                    discount_coupon=row.get('Cupón de descuento', ''),

                    # Notas
                    buyer_notes=row.get('Notas del comprador', ''),
                    seller_notes=row.get('Notas del vendedor', ''),

                    # Fechas adicionales
                    payment_date=parse_date_string(row.get('Fecha de pago')),
                    shipping_date=parse_date_string(row.get('Fecha de envío')),

                    # Información del producto
                    product_name=row.get('Nombre del producto', ''),
                    product_price=clean_decimal(row.get('Precio del producto')),
                    product_quantity=int(row.get('Cantidad del producto', 0) or 0),
                    sku=row.get('SKU', ''),

                    # Información adicional
                    channel=row.get('Canal', ''),
                    tracking_code=row.get('Código de tracking del envío', ''),
                    payment_transaction_id=row.get('Identificador de la transacción en el medio de pago', ''),
                    order_id=row.get('Identificador de la orden', ''),
                    is_physical_product=is_physical,

                    # Información de personal
                    registered_by=row.get('Persona que registró la venta', ''),
                    sales_branch=row.get('Sucursal de venta', ''),
                    seller=row.get('Vendedor', '')
                )

                income.save()
                count += 1
                if count % 100 == 0:
                    print(f"Procesados {count} registros...")

            except Exception as e:
                errors += 1
                print(f"Error al procesar fila: {e}")
                continue

    print(f"Importación completada. {count} registros importados con éxito. {errors} errores.")
    return count, errors


if __name__ == "__main__":
    # Ruta al archivo CSV (ajustar según la ubicación)
    file_path = "ruta/al/archivo/ventasf522156615244e6cb7d24eca264dda11.csv"
    import_csv(file_path)
