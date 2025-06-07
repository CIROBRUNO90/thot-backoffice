import requests

from datetime import datetime, timedelta
from django.conf import settings


from ..models import Income
from ..constants import OrderStatus, PaymentStatus, ShippingStatus


class TiendanubeAPI:
    """
    Clase para interactuar con la API de Tiendanube/Nuvemshop
    """
    BASE_URL = "https://api.tiendanube.com/v1"

    def __init__(self):
        self.store_id = settings.TIENDANUBE_STORE_ID
        self.access_token = settings.TIENDANUBE_ACCESS_TOKEN
        self.headers = {
            'Authentication': f'bearer {self.access_token}',
            'Content-Type': 'application/json',
            'User-Agent': 'Mi Backoffice Django (email@ejemplo.com)'
        }
        self.api_url = f"{self.BASE_URL}/{self.store_id}"

    def get_orders(self, since_date=None, status=None, page=1, per_page=50):
        """
        Obtiene los pedidos desde la API de Tiendanube

        Args:
            since_date: Fecha desde la cual obtener pedidos (formato: YYYY-MM-DD)
            status: Estado de los pedidos ('open', 'closed', 'cancelled')
            page: Número de página para la paginación
            per_page: Cantidad de registros por página

        Returns:
            List: Lista de pedidos obtenidos
        """
        url = f"{self.api_url}/orders"
        params = {
            'page': page,
            'per_page': per_page
        }

        if since_date:
            params['created_at_min'] = since_date

        if status:
            params['status'] = status

        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error al obtener pedidos: {response.status_code} - {response.text}")

    def get_products(self, page=1, per_page=50, updated_since=None):
        """
        Obtiene los productos desde la API de Tiendanube

        Args:
            page: Número de página para la paginación
            per_page: Cantidad de registros por página
            updated_since: Fecha desde la cual obtener productos actualizados (formato: YYYY-MM-DD)

        Returns:
            List: Lista de productos obtenidos
        """
        url = f"{self.api_url}/products"
        params = {
            'page': page,
            'per_page': per_page
        }

        if updated_since:
            params['updated_since'] = updated_since

        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error al obtener productos: {response.status_code} - {response.text}")

    def get_order_details(self, order_id):
        """
        Obtiene los detalles de un pedido específico

        Args:
            order_id: ID del pedido en Tiendanube

        Returns:
            Dict: Detalles del pedido
        """
        url = f"{self.api_url}/orders/{order_id}"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error al obtener detalles del pedido {order_id}: {response.status_code} - {response.text}")

    def import_orders_to_incomes(days_ago=30):
        """
        Importa los pedidos de Tiendanube al modelo Income

        Args:
            days_ago: Número de días hacia atrás para importar pedidos

        Returns:
            Tuple: (orders_created, orders_updated, errors)
        """
        created = 0
        updated = 0
        errors = 0

        # Calcular fecha desde la cual importar
        since_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')

        api = TiendanubeAPI()

        # Obtener todos los pedidos paginados
        page = 1
        while True:
            try:
                orders = api.get_orders(since_date=since_date, page=page, per_page=50)

                if not orders:
                    break

                for order in orders:
                    try:
                        # Obtener detalles completos del pedido si es necesario
                        order_details = api.get_order_details(order['id'])

                        # Mapear el estado del pedido a nuestras constantes
                        order_status = OrderStatus.OPEN
                        if order_details['status'] == 'closed':
                            order_status = OrderStatus.CLOSED
                        elif order_details['status'] == 'cancelled':
                            order_status = OrderStatus.CANCELLED

                        # Mapear el estado del pago
                        payment_status = PaymentStatus.PENDING
                        if order_details['payment_status'] == 'paid':
                            payment_status = PaymentStatus.PAID
                        elif order_details['payment_status'] == 'cancelled':
                            payment_status = PaymentStatus.CANCELLED

                        # Mapear el estado del envío
                        shipping_status = ShippingStatus.NOT_PACKAGED
                        if order_details['shipping_status'] == 'fulfilled':
                            shipping_status = ShippingStatus.SHIPPED
                        elif order_details['shipping_status'] == 'delivered':
                            shipping_status = ShippingStatus.DELIVERED

                        # Verificar si el pedido ya existe en nuestra base de datos
                        income, created_record = Income.objects.update_or_create(
                            order_id=str(order_details['id']),
                            defaults={
                                'order_number': str(order_details['number']),
                                'email': order_details['customer']['email'],
                                'date': datetime.fromisoformat(order_details['created_at'].replace('Z', '+00:00')).date(),
                                'order_status': order_status,
                                'payment_status': payment_status,
                                'shipping_status': shipping_status,
                                'currency': order_details['currency'],
                                'product_subtotal': order_details['subtotal'],
                                'discount': order_details.get('discount', 0) or 0,
                                'shipping_cost': order_details.get('shipping_cost', 0) or 0,
                                'total': order_details['total'],
                                'buyer_name': f"{order_details['customer']['name']} {order_details['customer'].get('lastname', '')}".strip(),
                                'tax_id': order_details['customer'].get('identification', ''),
                                'phone': order_details['customer'].get('phone', ''),
                                'shipping_name': order_details['shipping_address'].get('name', ''),
                                'shipping_phone': order_details['shipping_address'].get('phone', ''),
                                'address': order_details['shipping_address'].get('address', ''),
                                'address_number': order_details['shipping_address'].get('number', ''),
                                'floor_apt': f"{order_details['shipping_address'].get('floor', '')} {order_details['shipping_address'].get('apartment', '')}".strip(),
                                'city': order_details['shipping_address'].get('city', ''),
                                'postal_code': order_details['shipping_address'].get('zipcode', ''),
                                'state_province': order_details['shipping_address'].get('province', ''),
                                'country': order_details['shipping_address'].get('country', ''),
                                'shipping_method': order_details.get('shipping_option_name', ''),
                                'payment_method': order_details.get('payment_details', {}).get('method', ''),
                                'payment_transaction_id': order_details.get('payment_details', {}).get('transaction_id', ''),
                                # Nota: Para Tiendanube generalmente necesitarás crear múltiples registros de Income
                                # para un solo pedido si hay múltiples productos
                                'product_name': ', '.join([item['name'] for item in order_details['products']]),
                                'product_price': order_details['products'][0]['price'] if order_details['products'] else 0,
                                'product_quantity': sum([item['quantity'] for item in order_details['products']]),
                                'payment_date': datetime.fromisoformat(order_details['paid_at'].replace('Z', '+00:00')).date() if order_details.get('paid_at') else None,
                                'shipping_date': datetime.fromisoformat(order_details['shipped_at'].replace('Z', '+00:00')).date() if order_details.get('shipped_at') else None,
                                'channel': order_details.get('source', ''),
                                'tracking_code': order_details.get('tracking_number', ''),
                                'is_physical_product': True,  # Por defecto en Tiendanube
                            }
                        )

                        if created_record:
                            created += 1
                        else:
                            updated += 1

                    except Exception as e:
                        errors += 1
                        print(f"Error al procesar el pedido {order['id']}: {str(e)}")

                # Ir a la siguiente página
                page += 1

                # Si ya no hay más pedidos, salir del bucle
                if len(orders) < 50:
                    break

            except Exception as e:
                print(f"Error al obtener pedidos de la página {page}: {str(e)}")
                errors += 1
                break

        return created, updated, errors

    def import_all_orders_from_tiendanube():
        """
        Comando de gestión para importar todos los pedidos desde Tiendanube
        """
        created, updated, errors = import_orders_to_incomes(days_ago=365)  # Último año
        return f"Importación completada: {created} creados, {updated} actualizados, {errors} errores"
