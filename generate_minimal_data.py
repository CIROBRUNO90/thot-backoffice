#!/usr/bin/env python
"""
Script minimalista para generar datos de prueba básicos
Uso: python generate_minimal_data.py
"""

import os
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
    OrderStatus, PaymentStatus, PaymentMethod, BusinessType, Currency
)

User = get_user_model()
fake = Faker(['es_ES'])


def generate_minimal_data():
    """Genera datos mínimos para pruebas rápidas"""
    print('🚀 Generando datos mínimos de prueba...')
    
    try:
        with transaction.atomic():
            # 1. Crear un cliente
            customer = Customer.objects.create(
                name="Empresa de Prueba",
                email="test@empresa.com",
                phone="+54 11 1234-5678",
                address="Av. Corrientes 123, CABA"
            )
            print('✅ Cliente creado')
            
            # 2. Crear unidades de negocio
            units = []
            for i, name in enumerate(['Oficina Principal', 'Sucursal Centro', 'Tienda Online']):
                unit = BusinessUnit.objects.create(
                    customer=customer,
                    name=f"{customer.name} - {name}",
                    description=f"Unidad de negocio {name.lower()}",
                    is_active=True
                )
                units.append(unit)
            print('✅ Unidades de negocio creadas')
            
            # 3. Crear tipos de gastos básicos
            expense_types = []
            basic_types = [
                ('ALQ', 'Alquiler', 50000),
                ('SER', 'Servicios', 15000),
                ('SUE', 'Sueldos', 200000),
                ('IMP', 'Impuestos', 25000),
                ('MAT', 'Materiales', 30000),
            ]
            
            for code, name, limit in basic_types:
                expense_type = ExpenseType.objects.create(
                    code=code,
                    name=name,
                    limit=Decimal(limit)
                )
                expense_types.append(expense_type)
            print('✅ Tipos de gastos creados')
            
            # 4. Usar usuario existente o crear uno
            users = list(User.objects.all())
            if not users:
                user = User.objects.create_user(
                    username='testuser',
                    email='test@example.com',
                    first_name='Usuario',
                    last_name='Prueba',
                    password='testpass123'
                )
                users = [user]
            
            # 5. Asignar usuario a unidades
            for i, unit in enumerate(units):
                BusinessUnitUser.objects.create(
                    user=users[0],
                    business_unit=unit,
                    is_primary=(i == 0)
                )
            print('✅ Usuario asignado a unidades')
            
            # 6. Generar algunos gastos
            for i in range(20):
                date = datetime.now().date() - timedelta(days=random.randint(0, 365))
                Expenses.objects.create(
                    date=date,
                    business_unit=random.choice(units),
                    expense_type=random.choice(expense_types),
                    amount=Decimal(random.uniform(1000, 50000)).quantize(Decimal('0.01')),
                    is_fixed=random.choice([True, False]),
                    observations=f"Gasto de prueba {i+1}"
                )
            print('✅ Gastos generados')
            
            # 7. Generar algunos ingresos
            products = [
                ('Laptop HP', 150000, 'LAP001'),
                ('Mouse Inalámbrico', 5000, 'MOU001'),
                ('Teclado Mecánico', 15000, 'TEC001'),
                ('Monitor 24"', 80000, 'MON001'),
            ]
            
            for i in range(30):
                date = datetime.now().date() - timedelta(days=random.randint(0, 365))
                product_name, base_price, sku = random.choice(products)
                quantity = random.randint(1, 3)
                product_price = Decimal(base_price)
                product_subtotal = product_price * quantity
                discount = Decimal(random.uniform(0, float(product_subtotal * 0.2)))
                total = product_subtotal - discount
                
                Income.objects.create(
                    business_unit=random.choice(units),
                    order_number=f"ORD-{random.randint(1000, 9999)}",
                    date=date,
                    business_type=BusinessType.PHYSICAL,
                    order_status=OrderStatus.COMPLETED,
                    payment_status=PaymentStatus.PAID,
                    currency=Currency.ARS,
                    product_subtotal=product_subtotal,
                    discount=discount,
                    total=total,
                    buyer_name=fake.name(),
                    email=fake.email(),
                    payment_method=PaymentMethod.CASH,
                    payment_date=date,
                    product_name=product_name,
                    product_price=product_price,
                    product_quantity=quantity,
                    sku=sku,
                    is_physical_product=True,
                    channel='Local',
                    registered_by='Sistema',
                    seller='Vendedor 1'
                )
            print('✅ Ingresos generados')
            
        print('\n✅ Datos mínimos generados exitosamente!')
        print_summary()
        
    except Exception as e:
        print(f'❌ Error: {str(e)}')
        raise


def print_summary():
    """Imprime resumen de datos"""
    print('\n' + '='*40)
    print('📊 RESUMEN DE DATOS MÍNIMOS')
    print('='*40)
    
    print(f'🏢 Clientes: {Customer.objects.count()}')
    print(f'🏪 Unidades de Negocio: {BusinessUnit.objects.count()}')
    print(f'💰 Tipos de Gasto: {ExpenseType.objects.count()}')
    print(f'💸 Gastos: {Expenses.objects.count()}')
    print(f'💵 Ingresos: {Income.objects.count()}')
    print(f'👥 Usuarios: {User.objects.count()}')
    print(f'🔗 Asignaciones: {BusinessUnitUser.objects.count()}')
    
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
    
    print('='*40)


if __name__ == '__main__':
    generate_minimal_data() 