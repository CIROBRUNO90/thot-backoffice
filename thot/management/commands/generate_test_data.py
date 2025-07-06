from django.core.management.base import BaseCommand
from django.db import transaction, models
from django.contrib.auth import get_user_model
from decimal import Decimal
import random
from datetime import datetime, timedelta
import faker

from tenant.models import Customer, BusinessUnit, BusinessUnitUser
from expenses.models import ExpenseType, Expenses
from incomes.models import Income
from incomes.constants import (
    OrderStatus, PaymentStatus, ShippingStatus, PaymentMethod,
    ShippingMethod, BusinessType, Currency
)

User = get_user_model()


class Command(BaseCommand):
    help = 'Genera datos de prueba para el sistema de backoffice'

    def add_arguments(self, parser):
        parser.add_argument(
            '--expenses',
            type=int,
            default=500,
            help='Número de gastos a generar (default: 500)'
        )
        parser.add_argument(
            '--incomes',
            type=int,
            default=1000,
            help='Número de ingresos a generar (default: 1000)'
        )
        parser.add_argument(
            '--expense-types',
            type=int,
            default=15,
            help='Número de tipos de gasto a generar (default: 15)'
        )
        parser.add_argument(
            '--customers',
            type=int,
            default=8,
            help='Número de clientes a generar (default: 8)'
        )
        parser.add_argument(
            '--business-units-per-customer',
            type=int,
            default=3,
            help='Número de unidades de negocio por cliente (default: 3)'
        )
        parser.add_argument(
            '--users',
            type=int,
            default=30,
            help='Número de usuarios a generar (default: 30)'
        )
        parser.add_argument(
            '--start-date',
            type=str,
            default='2023-01-01',
            help='Fecha de inicio para los datos (YYYY-MM-DD)'
        )
        parser.add_argument(
            '--end-date',
            type=str,
            default='2024-12-31',
            help='Fecha de fin para los datos (YYYY-MM-DD)'
        )
        parser.add_argument(
            '--clear-existing',
            action='store_true',
            help='Eliminar datos existentes antes de generar nuevos'
        )

    def handle(self, *args, **options):
        self.fake = faker.Faker(['es_ES', 'en_US'])
        
        if options['clear_existing']:
            self.clear_existing_data()
        
        self.stdout.write(
            self.style.SUCCESS(
                '🚀 Iniciando generación de datos de prueba...'
            )
        )
        
        try:
            with transaction.atomic():
                # Generar datos base
                customers = self.generate_customers(options['customers'])
                business_units = self.generate_business_units(
                    customers, options['business_units_per_customer']
                )
                expense_types = self.generate_expense_types(options['expense_types'])
                users = self.generate_users(options['users'])
                self.assign_users_to_business_units(users, business_units)
                
                # Generar datos de volumen
                start_date = datetime.strptime(options['start_date'], '%Y-%m-%d').date()
                end_date = datetime.strptime(options['end_date'], '%Y-%m-%d').date()
                
                self.generate_expenses(
                    business_units, expense_types, options['expenses'], 
                    start_date, end_date
                )
                self.generate_incomes(
                    business_units, options['incomes'], start_date, end_date
                )
                
            self.stdout.write(
                self.style.SUCCESS('✅ Datos generados exitosamente!')
            )
            self.print_summary()
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error generando datos: {str(e)}')
            )
            raise

    def clear_existing_data(self):
        """Elimina datos existentes"""
        self.stdout.write('🗑️ Eliminando datos existentes...')
        
        Income.objects.all().delete()
        Expenses.objects.all().delete()
        ExpenseType.objects.all().delete()
        BusinessUnitUser.objects.all().delete()
        BusinessUnit.objects.all().delete()
        Customer.objects.all().delete()
        
        self.stdout.write('✅ Datos existentes eliminados')

    def generate_customers(self, count):
        """Genera clientes/empresas"""
        self.stdout.write(f'🏢 Generando {count} clientes...')
        
        customers = []
        used_names = set()
        used_emails = set()
        
        for i in range(count):
            # Generar nombre único
            while True:
                name = self.fake.company()[:255]
                if name not in used_names:
                    used_names.add(name)
                    break
            
            # Generar email único
            while True:
                email = self.fake.company_email()[:254]
                if email not in used_emails:
                    used_emails.add(email)
                    break
            
            customer = Customer.objects.create(
                name=name,
                email=email,
                phone=self.fake.phone_number()[:20],
                address=self.fake.address()
            )
            customers.append(customer)
        
        self.stdout.write(f'✅ {len(customers)} clientes generados')
        return customers

    def generate_business_units(self, customers, units_per_customer):
        """Genera unidades de negocio para cada cliente"""
        self.stdout.write(f'🏪 Generando unidades de negocio...')
        
        business_units = []
        unit_types = [
            'Sucursal Centro', 'Sucursal Norte', 'Sucursal Sur', 'Sucursal Este',
            'Sucursal Oeste', 'Oficina Principal', 'Depósito Central',
            'Tienda Online', 'Showroom', 'Almacén', 'Punto de Venta',
            'Sucursal Comercial', 'Sucursal Industrial', 'Sucursal Residencial'
        ]
        
        for customer in customers:
            used_unit_names = set()
            
            for i in range(units_per_customer):
                # Generar nombre único para esta empresa
                while True:
                    if i == 0:  # Primera unidad siempre activa
                        unit_name = f"{customer.name} - Oficina Principal"
                    else:
                        unit_type = random.choice(unit_types)
                        unit_name = f"{customer.name} - {unit_type}"
                    
                    if unit_name not in used_unit_names:
                        used_unit_names.add(unit_name)
                        break
                
                business_unit = BusinessUnit.objects.create(
                    customer=customer,
                    name=unit_name[:255],
                    description=self.fake.text(max_nb_chars=200),
                    is_active=random.choice([True, True, True, False])  # 75% activas
                )
                business_units.append(business_unit)
        
        self.stdout.write(f'✅ {len(business_units)} unidades de negocio generadas')
        return business_units

    def generate_expense_types(self, count):
        """Genera tipos de gastos"""
        self.stdout.write(f'💰 Generando {count} tipos de gastos...')
        
        expense_categories = [
            ('ALQ', 'Alquiler', 50000),
            ('SER', 'Servicios', 15000),
            ('SUE', 'Sueldos', 200000),
            ('IMP', 'Impuestos', 25000),
            ('MAT', 'Materiales', 30000),
            ('EQU', 'Equipamiento', 100000),
            ('MAR', 'Marketing', 20000),
            ('TRA', 'Transporte', 15000),
            ('SEG', 'Seguros', 12000),
            ('MAN', 'Mantenimiento', 18000),
            ('LIC', 'Licencias', 8000),
            ('CON', 'Consultoría', 25000),
            ('VIA', 'Viajes', 30000),
            ('OFI', 'Oficina', 12000),
            ('TEC', 'Tecnología', 40000),
            ('PRO', 'Proveedores', 35000),
            ('PUB', 'Publicidad', 15000),
            ('LEG', 'Legales', 20000),
            ('FIN', 'Financieros', 10000),
            ('OTR', 'Otros', 5000)
        ]
        
        expense_types = []
        for i in range(min(count, len(expense_categories))):
            code, name, limit = expense_categories[i]
            expense_type = ExpenseType.objects.create(
                code=code,
                name=name,
                limit=Decimal(limit)
            )
            expense_types.append(expense_type)
        
        self.stdout.write(f'✅ {len(expense_types)} tipos de gastos generados')
        return expense_types

    def generate_users(self, count):
        """Genera usuarios o usa existentes"""
        self.stdout.write(f'👥 Verificando usuarios...')
        
        existing_users = list(User.objects.all())
        if len(existing_users) >= count:
            self.stdout.write(f'✅ Usando {count} usuarios existentes')
            return random.sample(existing_users, count)
        
        # Si no hay suficientes usuarios, crear algunos
        users_to_create = count - len(existing_users)
        self.stdout.write(f'👤 Creando {users_to_create} usuarios adicionales...')
        
        used_usernames = set()
        used_emails = set()
        
        for i in range(users_to_create):
            # Generar username único
            while True:
                username = self.fake.user_name()
                if username not in used_usernames and not User.objects.filter(username=username).exists():
                    used_usernames.add(username)
                    break
            
            # Generar email único
            while True:
                email = self.fake.email()
                if email not in used_emails and not User.objects.filter(email=email).exists():
                    used_emails.add(email)
                    break
            
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=self.fake.first_name(),
                last_name=self.fake.last_name(),
                password='testpass123'
            )
            existing_users.append(user)
        
        self.stdout.write(f'✅ {len(existing_users)} usuarios disponibles')
        return existing_users

    def assign_users_to_business_units(self, users, business_units):
        """Asigna usuarios a unidades de negocio"""
        self.stdout.write('🔗 Asignando usuarios a unidades de negocio...')
        
        assignments = []
        active_units = [bu for bu in business_units if bu.is_active]
        
        for user in users:
            # Cada usuario puede estar en 1-3 unidades de negocio
            num_assignments = random.randint(1, min(3, len(active_units)))
            selected_units = random.sample(active_units, num_assignments)
            
            for i, unit in enumerate(selected_units):
                assignment = BusinessUnitUser.objects.create(
                    user=user,
                    business_unit=unit,
                    is_primary=(i == 0)  # Primera asignación es la principal
                )
                assignments.append(assignment)
        
        self.stdout.write(f'✅ {len(assignments)} asignaciones creadas')

    def generate_expenses(self, business_units, expense_types, count, start_date, end_date):
        """Genera gastos"""
        self.stdout.write(f'💸 Generando {count} gastos...')
        
        expenses = []
        active_units = [bu for bu in business_units if bu.is_active]
        
        for i in range(count):
            # Fecha aleatoria en el rango
            days_between = (end_date - start_date).days
            random_days = random.randint(0, days_between)
            expense_date = start_date + timedelta(days=random_days)
            
            # Unidad de negocio aleatoria
            business_unit = random.choice(active_units)
            
            # Tipo de gasto aleatorio
            expense_type = random.choice(expense_types)
            
            # Monto realista basado en el tipo
            base_amount = expense_type.limit or Decimal('10000')
            amount = Decimal(random.uniform(
                float(base_amount * Decimal('0.1')), 
                float(base_amount * Decimal('1.5'))
            )).quantize(Decimal('0.01'))
            
            expense = Expenses.objects.create(
                date=expense_date,
                business_unit=business_unit,
                expense_type=expense_type,
                amount=amount,
                is_fixed=random.choice([True, False, None]),
                observations=self.fake.text(max_nb_chars=150) if random.random() > 0.7 else ''
            )
            expenses.append(expense)
        
        self.stdout.write(f'✅ {len(expenses)} gastos generados')

    def generate_incomes(self, business_units, count, start_date, end_date):
        """Genera ingresos/ventas"""
        self.stdout.write(f'💵 Generando {count} ingresos...')
        
        incomes = []
        active_units = [bu for bu in business_units if bu.is_active]
        
        # Productos de ejemplo
        products = [
            ('Laptop HP', 150000, 'LAP001'),
            ('Mouse Inalámbrico', 5000, 'MOU001'),
            ('Teclado Mecánico', 15000, 'TEC001'),
            ('Monitor 24"', 80000, 'MON001'),
            ('Auriculares', 12000, 'AUR001'),
            ('Webcam HD', 8000, 'WEB001'),
            ('Impresora Láser', 45000, 'IMP001'),
            ('Tablet Samsung', 120000, 'TAB001'),
            ('Cable HDMI', 2000, 'CAB001'),
            ('Disco Externo 1TB', 25000, 'DIS001'),
            ('Servicio de Mantenimiento', 15000, 'SER001'),
            ('Consultoría IT', 50000, 'CON001'),
            ('Software Licencia', 30000, 'SOF001'),
            ('Reparación PC', 8000, 'REP001'),
            ('Instalación Red', 25000, 'INS001')
        ]
        
        for i in range(count):
            # Fecha aleatoria
            days_between = (end_date - start_date).days
            random_days = random.randint(0, days_between)
            income_date = start_date + timedelta(days=random_days)
            
            # Unidad de negocio aleatoria
            business_unit = random.choice(active_units)
            
            # Producto aleatorio
            product_name, base_price, sku = random.choice(products)
            
            # Cantidad y precios
            quantity = random.randint(1, 5)
            product_price = Decimal(base_price)
            product_subtotal = product_price * quantity
            
            # Descuento aleatorio
            discount = Decimal(random.uniform(0, float(product_subtotal * Decimal('0.3'))))
            
            # Envío
            shipping_cost = Decimal(random.uniform(0, 5000)) if random.random() > 0.5 else Decimal('0')
            
            # Total
            total = product_subtotal - discount + shipping_cost
            
            # Estados coherentes
            order_status = random.choice([
                OrderStatus.COMPLETED, OrderStatus.COMPLETED, OrderStatus.COMPLETED,
                OrderStatus.PROCESSING, OrderStatus.PENDING, OrderStatus.OPEN,
                OrderStatus.CANCELLED
            ])
            
            payment_status = random.choice([
                PaymentStatus.PAID, PaymentStatus.PAID, PaymentStatus.PAID,
                PaymentStatus.PENDING, PaymentStatus.PARTIALLY_PAID,
                PaymentStatus.FAILED
            ])
            
            # Método de pago
            payment_method = random.choice([
                PaymentMethod.CASH, PaymentMethod.CREDIT_CARD, PaymentMethod.DEBIT_CARD,
                PaymentMethod.MERCADO_PAGO, PaymentMethod.BANK_TRANSFER
            ])
            
            # Tipo de negocio
            business_type = random.choice([
                BusinessType.PHYSICAL, BusinessType.ECOMMERCE, BusinessType.MIXED
            ])
            
            # Moneda
            currency = random.choice([Currency.ARS, Currency.USD, Currency.EUR])
            
            # Generar tax_id respetando el límite de 20 caracteres
            tax_id = str(random.randint(10000000, 99999999))[:20]
            
            # Generar phone respetando el límite de 20 caracteres
            phone = self.fake.phone_number()[:20]
            
            # Generar channel respetando el límite de 50 caracteres
            channel = random.choice(['Local', 'Online', 'WhatsApp', 'Instagram', 'Facebook'])[:50]
            
            # Generar registered_by respetando el límite de 100 caracteres
            registered_by = random.choice(['Sistema', 'Vendedor 1', 'Vendedor 2', 'Admin'])[:100]
            
            # Generar seller respetando el límite de 100 caracteres
            seller = random.choice(['Vendedor 1', 'Vendedor 2', 'Vendedor 3', 'Auto'])[:100]
            
            income = Income.objects.create(
                business_unit=business_unit,
                order_number=f"ORD-{random.randint(10000, 99999)}",
                date=income_date,
                business_type=business_type,
                order_status=order_status,
                payment_status=payment_status,
                currency=currency,
                product_subtotal=product_subtotal,
                discount=discount,
                shipping_cost=shipping_cost,
                total=total,
                buyer_name=self.fake.name()[:255],
                email=self.fake.email()[:255],
                tax_id=tax_id,
                phone=phone,
                shipping_status=random.choice([
                    ShippingStatus.DELIVERED, ShippingStatus.SHIPPED,
                    ShippingStatus.NOT_REQUIRED, ShippingStatus.PACKAGED
                ]),
                shipping_method=random.choice([
                    ShippingMethod.DELIVERY, ShippingMethod.PICKUP,
                    ShippingMethod.STANDARD, ShippingMethod.NOT_REQUIRED
                ]),
                payment_method=payment_method,
                payment_date=income_date if payment_status == PaymentStatus.PAID else None,
                product_name=product_name[:255],
                product_price=product_price,
                product_quantity=quantity,
                sku=sku[:50],
                is_physical_product=random.choice([True, False]),
                channel=channel,
                registered_by=registered_by,
                seller=seller
            )
            incomes.append(income)
        
        self.stdout.write(f'✅ {len(incomes)} ingresos generados')

    def print_summary(self):
        """Imprime un resumen de los datos generados"""
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('📊 RESUMEN DE DATOS GENERADOS'))
        self.stdout.write('='*50)
        
        self.stdout.write(f'🏢 Clientes: {Customer.objects.count()}')
        self.stdout.write(f'🏪 Unidades de Negocio: {BusinessUnit.objects.count()}')
        self.stdout.write(f'💰 Tipos de Gasto: {ExpenseType.objects.count()}')
        self.stdout.write(f'💸 Gastos: {Expenses.objects.count()}')
        self.stdout.write(f'💵 Ingresos: {Income.objects.count()}')
        self.stdout.write(f'👥 Usuarios: {User.objects.count()}')
        self.stdout.write(f'🔗 Asignaciones Usuario-Unidad: {BusinessUnitUser.objects.count()}')
        
        # Estadísticas adicionales
        if Expenses.objects.exists():
            total_expenses = Expenses.objects.aggregate(
                total=models.Sum('amount')
            )['total'] or 0
            self.stdout.write(f'💸 Total Gastos: ${total_expenses:,.2f}')
        
        if Income.objects.exists():
            total_income = Income.objects.aggregate(
                total=models.Sum('total')
            )['total'] or 0
            self.stdout.write(f'💵 Total Ingresos: ${total_income:,.2f}')
        
        self.stdout.write('='*50) 