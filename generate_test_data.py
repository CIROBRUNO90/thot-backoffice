#!/usr/bin/env python
"""
Script para generar datos de prueba para el sistema de backoffice
Uso: python generate_test_data.py
"""

import os
import sys
import django
from decimal import Decimal
import random
from datetime import datetime, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thot-backoffice.settings')
django.setup()

from django.db import transaction, models
from django.contrib.auth import get_user_model
from faker import Faker

from tenant.models import Customer, BusinessUnit, BusinessUnitUser
from expenses.models import ExpenseType, Expenses
from incomes.models import Income
from incomes.constants import (
    OrderStatus, PaymentStatus, ShippingStatus, PaymentMethod,
    ShippingMethod, BusinessType, Currency
)

User = get_user_model()
fake = Faker(['es_ES', 'en_US'])


def clear_existing_data():
    """Elimina datos existentes"""
    print('🗑️ Eliminando datos existentes...')
    
    Income.objects.all().delete()
    Expenses.objects.all().delete()
    ExpenseType.objects.all().delete()
    BusinessUnitUser.objects.all().delete()
    BusinessUnit.objects.all().delete()
    Customer.objects.all().delete()
    
    print('✅ Datos existentes eliminados')


def generate_customers(count=8):
    """Genera clientes/empresas"""
    print(f'🏢 Generando {count} clientes...')
    
    customers = []
    for i in range(count):
        customer = Customer.objects.create(
            name=fake.company(),
            email=fake.company_email(),
            phone=fake.phone_number(),
            address=fake.address()
        )
        customers.append(customer)
    
    print(f'✅ {len(customers)} clientes generados')
    return customers


def generate_business_units(customers, units_per_customer=3):
    """Genera unidades de negocio para cada cliente"""
    print(f'🏪 Generando unidades de negocio...')
    
    business_units = []
    unit_types = [
        'Sucursal Centro', 'Sucursal Norte', 'Sucursal Sur', 'Sucursal Este',
        'Sucursal Oeste', 'Oficina Principal', 'Depósito Central',
        'Tienda Online', 'Showroom', 'Almacén', 'Punto de Venta',
        'Sucursal Comercial', 'Sucursal Industrial', 'Sucursal Residencial'
    ]
    
    for customer in customers:
        for i in range(units_per_customer):
            unit_name = f"{customer.name} - {random.choice(unit_types)}"
            if i == 0:  # Primera unidad siempre activa
                unit_name = f"{customer.name} - Oficina Principal"
            
            business_unit = BusinessUnit.objects.create(
                customer=customer,
                name=unit_name,
                description=fake.text(max_nb_chars=200),
                is_active=random.choice([True, True, True, False])  # 75% activas
            )
            business_units.append(business_unit)
    
    print(f'✅ {len(business_units)} unidades de negocio generadas')
    return business_units


def generate_expense_types(count=15):
    """Genera tipos de gastos"""
    print(f'💰 Generando {count} tipos de gastos...')
    
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
        ('MANT', 'Mantenimiento', 18000),
        ('LIC', 'Licencias', 8000),
        ('CONS', 'Consultoría', 25000),
        ('VIAJ', 'Viajes', 30000),
        ('OFIC', 'Oficina', 12000),
        ('TEC', 'Tecnología', 40000),
        ('PROV', 'Proveedores', 35000),
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
    
    print(f'✅ {len(expense_types)} tipos de gastos generados')
    return expense_types


def generate_users(count=30):
    """Genera usuarios o usa existentes"""
    print(f'👥 Verificando usuarios...')
    
    existing_users = list(User.objects.all())
    if len(existing_users) >= count:
        print(f'✅ Usando {count} usuarios existentes')
        return random.sample(existing_users, count)
    
    # Si no hay suficientes usuarios, crear algunos
    users_to_create = count - len(existing_users)
    print(f'👤 Creando {users_to_create} usuarios adicionales...')
    
    for i in range(users_to_create):
        username = fake.user_name()
        while User.objects.filter(username=username).exists():
            username = fake.user_name()
        
        user = User.objects.create_user(
            username=username,
            email=fake.email(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            password='testpass123'
        )
        existing_users.append(user)
    
    print(f'✅ {len(existing_users)} usuarios disponibles')
    return existing_users


def assign_users_to_business_units(users, business_units):
    """Asigna usuarios a unidades de negocio"""
    print('🔗 Asignando usuarios a unidades de negocio...')
    
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
    
    print(f'✅ {len(assignments)} asignaciones creadas')


def generate_expenses(business_units, expense_types, count=500, 
                     start_date=None, end_date=None):
    """Genera gastos"""
    print(f'💸 Generando {count} gastos...')
    
    if not start_date:
        start_date = datetime(2023, 1, 1).date()
    if not end_date:
        end_date = datetime(2024, 12, 31).date()
    
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
            observations=fake.text(max_nb_chars=150) if random.random() > 0.7 else ''
        )
        expenses.append(expense)
    
    print(f'✅ {len(expenses)} gastos generados')


def generate_incomes(business_units, count=1000, start_date=None, end_date=None):
    """Genera ingresos/ventas"""
    print(f'💵 Generando {count} ingresos...')
    
    if not start_date:
        start_date = datetime(2023, 1, 1).date()
    if not end_date:
        end_date = datetime(2024, 12, 31).date()
    
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
            buyer_name=fake.name(),
            email=fake.email(),
            tax_id=str(random.randint(10000000, 99999999)),
            phone=fake.phone_number(),
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
            product_name=product_name,
            product_price=product_price,
            product_quantity=quantity,
            sku=sku,
            is_physical_product=random.choice([True, False]),
            channel=random.choice(['Local', 'Online', 'WhatsApp', 'Instagram', 'Facebook']),
            registered_by=random.choice(['Sistema', 'Vendedor 1', 'Vendedor 2', 'Admin']),
            seller=random.choice(['Vendedor 1', 'Vendedor 2', 'Vendedor 3', 'Auto'])
        )
        incomes.append(income)
    
    print(f'✅ {len(incomes)} ingresos generados')


def print_summary():
    """Imprime un resumen de los datos generados"""
    print('\n' + '='*50)
    print('📊 RESUMEN DE DATOS GENERADOS')
    print('='*50)
    
    print(f'🏢 Clientes: {Customer.objects.count()}')
    print(f'🏪 Unidades de Negocio: {BusinessUnit.objects.count()}')
    print(f'💰 Tipos de Gasto: {ExpenseType.objects.count()}')
    print(f'💸 Gastos: {Expenses.objects.count()}')
    print(f'💵 Ingresos: {Income.objects.count()}')
    print(f'👥 Usuarios: {User.objects.count()}')
    print(f'🔗 Asignaciones Usuario-Unidad: {BusinessUnitUser.objects.count()}')
    
    # Estadísticas adicionales
    if Expenses.objects.exists():
        total_expenses = Expenses.objects.aggregate(
            total=models.Sum('amount')
        )['total'] or 0
        print(f'💸 Total Gastos: ${total_expenses:,.2f}')
    
    if Income.objects.exists():
        total_income = Income.objects.aggregate(
            total=models.Sum('total')
        )['total'] or 0
        print(f'💵 Total Ingresos: ${total_income:,.2f}')
    
    print('='*50)


def main():
    """Función principal"""
    print('🚀 Iniciando generación de datos de prueba...')
    
    # Verificar si queremos limpiar datos existentes
    if len(sys.argv) > 1 and sys.argv[1] == '--clear':
        clear_existing_data()
    
    try:
        with transaction.atomic():
            # Generar datos base
            customers = generate_customers(8)
            business_units = generate_business_units(customers, 3)
            expense_types = generate_expense_types(15)
            users = generate_users(30)
            assign_users_to_business_units(users, business_units)
            
            # Generar datos de volumen
            start_date = datetime(2023, 1, 1).date()
            end_date = datetime(2024, 12, 31).date()
            
            generate_expenses(business_units, expense_types, 500, start_date, end_date)
            generate_incomes(business_units, 1000, start_date, end_date)
            
        print('✅ Datos generados exitosamente!')
        print_summary()
        
    except Exception as e:
        print(f'❌ Error generando datos: {str(e)}')
        raise


if __name__ == '__main__':
    main() 