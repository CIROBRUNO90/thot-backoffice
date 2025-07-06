# Generador de Datos de Prueba

Este script genera datos de prueba realistas para el sistema de backoffice, respetando las relaciones entre modelos y la integridad de la base de datos.

## 📋 Requisitos

1. **Instalar Faker** (si no está instalado):
```bash
pip install Faker==24.2.0
```

2. **Configurar la base de datos** (asegúrate de que Django esté configurado correctamente)

## 🚀 Uso

### Opción 1: Management Command de Django (Recomendado)
```bash
# Generar datos básicos
python manage.py generate_test_data

# Con opciones personalizadas
python manage.py generate_test_data --expenses 1000 --incomes 2000 --customers 10

# Limpiar y regenerar
python manage.py generate_test_data --clear-existing
```

### Opción 2: Script Python Independiente
```bash
# Generar datos básicos (recomendado para empezar)
python generate_test_data.py

# Limpiar datos existentes y generar nuevos
python generate_test_data.py --clear
```



## 📊 Datos Generados

### Datos Base (Pocos registros)
- **8 Clientes/Empresas** con información realista
- **24 Unidades de Negocio** (3 por cliente)
- **15 Tipos de Gastos** con códigos y límites
- **30 Usuarios** (usa existentes o crea nuevos)
- **Asignaciones Usuario-Unidad** (1-3 unidades por usuario)

### Datos de Volumen (Muchos registros)
- **500 Gastos** distribuidos entre unidades activas
- **1000 Ingresos/Ventas** con información completa
- **Fechas**: 2023-2024 (distribuidas aleatoriamente)

## 🎯 Características de los Datos

### Gastos
- ✅ Montos realistas basados en el tipo de gasto
- ✅ Fechas distribuidas en el rango especificado
- ✅ Solo unidades de negocio activas
- ✅ Observaciones opcionales
- ✅ Gastos fijos y variables

### Ingresos/Ventas
- ✅ 15 productos diferentes con precios realistas
- ✅ Estados de orden coherentes (70% completadas)
- ✅ Estados de pago realistas (70% pagadas)
- ✅ Métodos de pago variados
- ✅ Información de envío completa
- ✅ Diferentes tipos de negocio (físico, e-commerce, mixto)
- ✅ Múltiples monedas (ARS, USD, EUR)
- ✅ Canales de venta variados

### Relaciones
- ✅ Usuarios asignados a múltiples unidades
- ✅ Unidad principal por usuario
- ✅ Gastos e ingresos vinculados a unidades activas
- ✅ Integridad referencial mantenida

## ⚙️ Opciones de Personalización

### Management Command
```bash
python manage.py generate_test_data \
    --expenses 1000 \
    --incomes 2000 \
    --customers 10 \
    --business-units-per-customer 5 \
    --users 50 \
    --expense-types 20 \
    --start-date 2022-01-01 \
    --end-date 2024-12-31 \
    --clear-existing
```

### Script Python
Modifica las variables en la función `main()`:
```python
customers = generate_customers(10)  # 10 clientes
business_units = generate_business_units(customers, 5)  # 5 unidades por cliente
expense_types = generate_expense_types(20)  # 20 tipos de gasto
users = generate_users(50)  # 50 usuarios
generate_expenses(business_units, expense_types, 1000)  # 1000 gastos
generate_incomes(business_units, 2000)  # 2000 ingresos
```

## 📈 Ejemplo de Salida

```
🚀 Iniciando generación de datos de prueba...
🏢 Generando 8 clientes...
✅ 8 clientes generados
🏪 Generando unidades de negocio...
✅ 24 unidades de negocio generadas
💰 Generando 15 tipos de gastos...
✅ 15 tipos de gastos generados
👥 Verificando usuarios...
✅ 30 usuarios disponibles
🔗 Asignando usuarios a unidades de negocio...
✅ 75 asignaciones creadas
💸 Generando 500 gastos...
✅ 500 gastos generados
💵 Generando 1000 ingresos...
✅ 1000 ingresos generados
✅ Datos generados exitosamente!

==================================================
📊 RESUMEN DE DATOS GENERADOS
==================================================
🏢 Clientes: 8
🏪 Unidades de Negocio: 24
💰 Tipos de Gasto: 15
💸 Gastos: 500
💵 Ingresos: 1000
👥 Usuarios: 30
🔗 Asignaciones Usuario-Unidad: 75
💸 Total Gastos: $12,345,678.90
💵 Total Ingresos: $45,678,901.23
==================================================
```

## 🔧 Solución de Problemas

### Error: "No module named 'faker'"
```bash
pip install Faker==24.2.0
```

### Error: "Settings module not found"
Asegúrate de estar en el directorio correcto:
```bash
cd thot-backoffice
python generate_test_data.py
```

### Error: "Database connection"
Verifica que tu base de datos esté configurada y accesible.

### Datos duplicados
Usa la opción `--clear` o `--clear-existing` para limpiar datos existentes.

## 💡 Consejos

1. **Primera ejecución**: Usa los valores por defecto para probar
2. **Volumen grande**: Incrementa gradualmente los números
3. **Fechas**: Ajusta el rango según tus necesidades de prueba
4. **Backup**: Haz backup de tu base de datos antes de usar `--clear`
5. **Desarrollo**: Los datos generados son perfectos para desarrollo y testing

## 🎨 Personalización Avanzada

### Agregar Nuevos Tipos de Gastos
Modifica la lista `expense_categories` en `generate_expense_types()`:
```python
expense_categories = [
    ('ALQ', 'Alquiler', 50000),
    ('SER', 'Servicios', 15000),
    # Agregar nuevos aquí...
    ('NUEVO', 'Nuevo Tipo', 25000),
]
```

### Agregar Nuevos Productos
Modifica la lista `products` en `generate_incomes()`:
```python
products = [
    ('Laptop HP', 150000, 'LAP001'),
    # Agregar nuevos aquí...
    ('Nuevo Producto', 75000, 'NUE001'),
]
```

### Cambiar Distribución de Estados
Modifica las probabilidades en `generate_incomes()`:
```python
order_status = random.choice([
    OrderStatus.COMPLETED, OrderStatus.COMPLETED, OrderStatus.COMPLETED,  # 3/7 = 43%
    OrderStatus.PROCESSING, OrderStatus.PENDING, OrderStatus.OPEN,      # 3/7 = 43%
    OrderStatus.CANCELLED                                               # 1/7 = 14%
])
``` 