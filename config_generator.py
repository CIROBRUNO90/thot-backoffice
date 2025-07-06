#!/usr/bin/env python
"""
Archivo de configuración para personalizar la generación de datos de prueba
Modifica estos valores según tus necesidades
"""

# =============================================================================
# CONFIGURACIÓN DE DATOS BASE
# =============================================================================

# Número de clientes/empresas a generar
CUSTOMERS_COUNT = 8

# Número de unidades de negocio por cliente
BUSINESS_UNITS_PER_CUSTOMER = 3

# Número de tipos de gastos a generar
EXPENSE_TYPES_COUNT = 15

# Número de usuarios a usar/crear
USERS_COUNT = 30

# =============================================================================
# CONFIGURACIÓN DE DATOS DE VOLUMEN
# =============================================================================

# Número de gastos a generar
EXPENSES_COUNT = 500

# Número de ingresos/ventas a generar
INCOMES_COUNT = 1000

# =============================================================================
# CONFIGURACIÓN DE FECHAS
# =============================================================================

# Fecha de inicio para los datos (YYYY-MM-DD)
START_DATE = '2023-01-01'

# Fecha de fin para los datos (YYYY-MM-DD)
END_DATE = '2024-12-31'

# =============================================================================
# CONFIGURACIÓN DE TIPOS DE GASTOS
# =============================================================================

# Lista de tipos de gastos con código, nombre y límite
EXPENSE_CATEGORIES = [
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

# =============================================================================
# CONFIGURACIÓN DE PRODUCTOS
# =============================================================================

# Lista de productos con nombre, precio base y SKU
PRODUCTS = [
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

# =============================================================================
# CONFIGURACIÓN DE PROBABILIDADES
# =============================================================================

# Probabilidad de que una unidad de negocio esté activa (0.0 a 1.0)
ACTIVE_BUSINESS_UNIT_PROBABILITY = 0.75

# Probabilidad de que un gasto sea fijo (0.0 a 1.0)
FIXED_EXPENSE_PROBABILITY = 0.6

# Probabilidad de que un gasto tenga observaciones (0.0 a 1.0)
EXPENSE_WITH_OBSERVATIONS_PROBABILITY = 0.3

# Probabilidad de que un ingreso tenga envío (0.0 a 1.0)
INCOME_WITH_SHIPPING_PROBABILITY = 0.5

# Probabilidad de que un producto sea físico (0.0 a 1.0)
PHYSICAL_PRODUCT_PROBABILITY = 0.7

# =============================================================================
# CONFIGURACIÓN DE RANGOS
# =============================================================================

# Rango de cantidades de producto (mínimo, máximo)
PRODUCT_QUANTITY_RANGE = (1, 5)

# Rango de descuentos como porcentaje del subtotal (mínimo, máximo)
DISCOUNT_PERCENTAGE_RANGE = (0.0, 0.3)

# Rango de costos de envío (mínimo, máximo)
SHIPPING_COST_RANGE = (0, 5000)

# Rango de asignaciones de usuario por unidad de negocio (mínimo, máximo)
USER_ASSIGNMENTS_RANGE = (1, 3)

# =============================================================================
# CONFIGURACIÓN DE CANALES DE VENTA
# =============================================================================

SALES_CHANNELS = [
    'Local',
    'Online', 
    'WhatsApp',
    'Instagram',
    'Facebook',
    'Telegram',
    'Email',
    'Teléfono'
]

# =============================================================================
# CONFIGURACIÓN DE VENDEDORES
# =============================================================================

SELLERS = [
    'Vendedor 1',
    'Vendedor 2', 
    'Vendedor 3',
    'Auto',
    'Sistema',
    'Admin'
]

# =============================================================================
# CONFIGURACIÓN DE TIPOS DE UNIDADES DE NEGOCIO
# =============================================================================

BUSINESS_UNIT_TYPES = [
    'Sucursal Centro',
    'Sucursal Norte', 
    'Sucursal Sur',
    'Sucursal Este',
    'Sucursal Oeste',
    'Oficina Principal',
    'Depósito Central',
    'Tienda Online',
    'Showroom',
    'Almacén',
    'Punto de Venta',
    'Sucursal Comercial',
    'Sucursal Industrial',
    'Sucursal Residencial'
]

# =============================================================================
# CONFIGURACIÓN DE MONEDAS (peso de probabilidad)
# =============================================================================

CURRENCY_WEIGHTS = {
    'ARS': 0.7,  # 70% peso argentino
    'USD': 0.2,  # 20% dólar
    'EUR': 0.1   # 10% euro
}

# =============================================================================
# CONFIGURACIÓN DE ESTADOS (peso de probabilidad)
# =============================================================================

ORDER_STATUS_WEIGHTS = {
    'completada': 0.7,      # 70% completadas
    'procesando': 0.15,     # 15% procesando
    'pendiente': 0.1,       # 10% pendiente
    'abierta': 0.03,        # 3% abierta
    'cancelada': 0.02       # 2% cancelada
}

PAYMENT_STATUS_WEIGHTS = {
    'pagado': 0.7,          # 70% pagado
    'pendiente': 0.2,       # 20% pendiente
    'parcialmente_pagado': 0.08,  # 8% parcialmente pagado
    'fallido': 0.02         # 2% fallido
}

# =============================================================================
# CONFIGURACIÓN DE MÉTODOS DE PAGO (peso de probabilidad)
# =============================================================================

PAYMENT_METHOD_WEIGHTS = {
    'efectivo': 0.3,        # 30% efectivo
    'tarjeta_credito': 0.25, # 25% tarjeta crédito
    'tarjeta_debito': 0.2,   # 20% tarjeta débito
    'mercado_pago': 0.15,    # 15% mercado pago
    'transferencia': 0.1     # 10% transferencia
}

# =============================================================================
# CONFIGURACIÓN DE TIPOS DE NEGOCIO (peso de probabilidad)
# =============================================================================

BUSINESS_TYPE_WEIGHTS = {
    'fisico': 0.4,          # 40% físico
    'ecommerce': 0.35,      # 35% e-commerce
    'mixto': 0.25           # 25% mixto
} 