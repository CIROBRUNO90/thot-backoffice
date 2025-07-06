-- Script SQL para generar datos de prueba básicos
-- Uso: psql -d tu_base_de_datos -f generate_test_data.sql

-- Limpiar datos existentes (opcional - descomenta si necesitas)
-- DELETE FROM incomes_income;
-- DELETE FROM expenses_expenses;
-- DELETE FROM expenses_expensetype;
-- DELETE FROM tenant_businessunituser;
-- DELETE FROM tenant_businessunit;
-- DELETE FROM tenant_customer;

-- Insertar clientes
INSERT INTO tenant_customer (name, email, phone, address, created_at, updated_at) VALUES
('TechCorp Argentina', 'info@techcorp.com.ar', '+54 11 1234-5678', 'Av. Corrientes 1234, CABA', NOW(), NOW()),
('Digital Solutions SA', 'contacto@digitalsolutions.com', '+54 11 2345-6789', 'Florida 567, CABA', NOW(), NOW()),
('Innovación Tecnológica', 'info@innovacion.com', '+54 11 3456-7890', 'Lavalle 890, CABA', NOW(), NOW()),
('Software Factory', 'hello@softwarefactory.com', '+54 11 4567-8901', 'Reconquista 234, CABA', NOW(), NOW()),
('Data Analytics Pro', 'info@dataanalytics.com', '+54 11 5678-9012', 'San Martín 456, CABA', NOW(), NOW());

-- Insertar unidades de negocio
INSERT INTO tenant_businessunit (customer_id, name, description, is_active, created_at, updated_at) VALUES
-- TechCorp Argentina
(1, 'TechCorp Argentina - Oficina Principal', 'Sede central de TechCorp', true, NOW(), NOW()),
(1, 'TechCorp Argentina - Sucursal Centro', 'Sucursal en el centro de la ciudad', true, NOW(), NOW()),
(1, 'TechCorp Argentina - Tienda Online', 'Plataforma de ventas online', true, NOW(), NOW()),

-- Digital Solutions SA
(2, 'Digital Solutions SA - Oficina Principal', 'Sede principal de Digital Solutions', true, NOW(), NOW()),
(2, 'Digital Solutions SA - Sucursal Norte', 'Sucursal en zona norte', true, NOW(), NOW()),
(2, 'Digital Solutions SA - Depósito Central', 'Almacén y logística', false, NOW(), NOW()),

-- Innovación Tecnológica
(3, 'Innovación Tecnológica - Oficina Principal', 'Sede central de Innovación', true, NOW(), NOW()),
(3, 'Innovación Tecnológica - Sucursal Sur', 'Sucursal en zona sur', true, NOW(), NOW()),
(3, 'Innovación Tecnológica - Showroom', 'Espacio de exhibición', true, NOW(), NOW()),

-- Software Factory
(4, 'Software Factory - Oficina Principal', 'Sede principal de Software Factory', true, NOW(), NOW()),
(4, 'Software Factory - Sucursal Este', 'Sucursal en zona este', true, NOW(), NOW()),
(4, 'Software Factory - Laboratorio', 'Centro de desarrollo', true, NOW(), NOW()),

-- Data Analytics Pro
(5, 'Data Analytics Pro - Oficina Principal', 'Sede central de Data Analytics', true, NOW(), NOW()),
(5, 'Data Analytics Pro - Sucursal Oeste', 'Sucursal en zona oeste', true, NOW(), NOW()),
(5, 'Data Analytics Pro - Centro de Datos', 'Infraestructura de datos', false, NOW(), NOW());

-- Insertar tipos de gastos
INSERT INTO expenses_expensetype (code, name, limit, created_at, updated_at) VALUES
('ALQ', 'Alquiler', 50000.00, NOW(), NOW()),
('SER', 'Servicios', 15000.00, NOW(), NOW()),
('SUE', 'Sueldos', 200000.00, NOW(), NOW()),
('IMP', 'Impuestos', 25000.00, NOW(), NOW()),
('MAT', 'Materiales', 30000.00, NOW(), NOW()),
('EQU', 'Equipamiento', 100000.00, NOW(), NOW()),
('MAR', 'Marketing', 20000.00, NOW(), NOW()),
('TRA', 'Transporte', 15000.00, NOW(), NOW()),
('SEG', 'Seguros', 12000.00, NOW(), NOW()),
('MANT', 'Mantenimiento', 18000.00, NOW(), NOW()),
('LIC', 'Licencias', 8000.00, NOW(), NOW()),
('CONS', 'Consultoría', 25000.00, NOW(), NOW()),
('VIAJ', 'Viajes', 30000.00, NOW(), NOW()),
('OFIC', 'Oficina', 12000.00, NOW(), NOW()),
('TEC', 'Tecnología', 40000.00, NOW(), NOW());

-- Insertar gastos de ejemplo (últimos 6 meses)
INSERT INTO expenses_expenses (date, business_unit_id, expense_type_id, amount, is_fixed, observations, created_at, updated_at) VALUES
-- Gastos de TechCorp
('2024-01-15', 1, 1, 45000.00, true, 'Alquiler oficina principal', NOW(), NOW()),
('2024-01-20', 1, 2, 12000.00, true, 'Servicios básicos', NOW(), NOW()),
('2024-02-01', 1, 3, 180000.00, true, 'Sueldos personal', NOW(), NOW()),
('2024-02-15', 2, 4, 22000.00, true, 'Impuestos municipales', NOW(), NOW()),
('2024-03-01', 2, 5, 25000.00, false, 'Materiales de oficina', NOW(), NOW()),
('2024-03-15', 3, 6, 80000.00, false, 'Equipos informáticos', NOW(), NOW()),

-- Gastos de Digital Solutions
('2024-01-10', 4, 1, 52000.00, true, 'Alquiler sede principal', NOW(), NOW()),
('2024-01-25', 4, 2, 14000.00, true, 'Servicios y mantenimiento', NOW(), NOW()),
('2024-02-05', 5, 3, 160000.00, true, 'Nómina de empleados', NOW(), NOW()),
('2024-02-20', 5, 7, 18000.00, false, 'Campaña publicitaria', NOW(), NOW()),
('2024-03-05', 4, 8, 12000.00, false, 'Transporte y logística', NOW(), NOW()),
('2024-03-20', 5, 9, 10000.00, true, 'Seguro empresarial', NOW(), NOW()),

-- Gastos de Innovación Tecnológica
('2024-01-12', 7, 1, 48000.00, true, 'Alquiler oficina central', NOW(), NOW()),
('2024-01-28', 7, 2, 11000.00, true, 'Servicios básicos', NOW(), NOW()),
('2024-02-08', 8, 3, 140000.00, true, 'Sueldos del personal', NOW(), NOW()),
('2024-02-25', 8, 10, 15000.00, false, 'Mantenimiento equipos', NOW(), NOW()),
('2024-03-10', 9, 11, 6000.00, false, 'Licencias software', NOW(), NOW()),
('2024-03-25', 7, 12, 20000.00, false, 'Consultoría externa', NOW(), NOW()),

-- Gastos de Software Factory
('2024-01-18', 10, 1, 55000.00, true, 'Alquiler sede principal', NOW(), NOW()),
('2024-01-30', 10, 2, 13000.00, true, 'Servicios de oficina', NOW(), NOW()),
('2024-02-12', 11, 3, 170000.00, true, 'Nómina completa', NOW(), NOW()),
('2024-02-28', 11, 13, 25000.00, false, 'Viajes de negocios', NOW(), NOW()),
('2024-03-12', 12, 14, 10000.00, false, 'Suministros oficina', NOW(), NOW()),
('2024-03-28', 10, 15, 35000.00, false, 'Equipos tecnológicos', NOW(), NOW()),

-- Gastos de Data Analytics Pro
('2024-01-22', 13, 1, 50000.00, true, 'Alquiler oficina central', NOW(), NOW()),
('2024-02-02', 13, 2, 12000.00, true, 'Servicios básicos', NOW(), NOW()),
('2024-02-18', 14, 3, 150000.00, true, 'Sueldos empleados', NOW(), NOW()),
('2024-03-02', 14, 4, 23000.00, true, 'Impuestos y cargas', NOW(), NOW()),
('2024-03-18', 13, 5, 28000.00, false, 'Materiales de trabajo', NOW(), NOW()),
('2024-03-30', 14, 6, 90000.00, false, 'Equipamiento especializado', NOW(), NOW());

-- Insertar ingresos de ejemplo (últimos 6 meses)
INSERT INTO incomes_income (
    business_unit_id, order_number, date, business_type, order_status, payment_status, 
    currency, product_subtotal, discount, shipping_cost, total, buyer_name, email, 
    tax_id, phone, payment_method, payment_date, product_name, product_price, 
    product_quantity, sku, is_physical_product, channel, registered_by, seller, 
    created_at, updated_at
) VALUES
-- Ingresos de TechCorp
(1, 'ORD-10001', '2024-01-15', 'fisico', 'completada', 'pagado', 'ARS', 150000.00, 0.00, 0.00, 150000.00, 'Juan Pérez', 'juan@email.com', '12345678', '+54 11 1111-1111', 'efectivo', '2024-01-15', 'Laptop HP', 150000.00, 1, 'LAP001', true, 'Local', 'Sistema', 'Vendedor 1', NOW(), NOW()),
(2, 'ORD-10002', '2024-01-20', 'ecommerce', 'completada', 'pagado', 'ARS', 5000.00, 500.00, 1000.00, 5500.00, 'María García', 'maria@email.com', '23456789', '+54 11 2222-2222', 'tarjeta_credito', '2024-01-20', 'Mouse Inalámbrico', 5000.00, 1, 'MOU001', true, 'Online', 'Sistema', 'Vendedor 2', NOW(), NOW()),
(3, 'ORD-10003', '2024-02-01', 'mixto', 'completada', 'pagado', 'USD', 80000.00, 8000.00, 0.00, 72000.00, 'Carlos López', 'carlos@email.com', '34567890', '+54 11 3333-3333', 'mercado_pago', '2024-02-01', 'Monitor 24"', 80000.00, 1, 'MON001', true, 'WhatsApp', 'Sistema', 'Vendedor 1', NOW(), NOW()),

-- Ingresos de Digital Solutions
(4, 'ORD-10004', '2024-02-10', 'fisico', 'completada', 'pagado', 'ARS', 120000.00, 0.00, 0.00, 120000.00, 'Ana Rodríguez', 'ana@email.com', '45678901', '+54 11 4444-4444', 'efectivo', '2024-02-10', 'Tablet Samsung', 120000.00, 1, 'TAB001', true, 'Local', 'Sistema', 'Vendedor 3', NOW(), NOW()),
(5, 'ORD-10005', '2024-02-25', 'ecommerce', 'completada', 'pagado', 'ARS', 15000.00, 1500.00, 2000.00, 15500.00, 'Luis Martínez', 'luis@email.com', '56789012', '+54 11 5555-5555', 'tarjeta_debito', '2024-02-25', 'Teclado Mecánico', 15000.00, 1, 'TEC001', true, 'Online', 'Sistema', 'Vendedor 2', NOW(), NOW()),
(4, 'ORD-10006', '2024-03-05', 'mixto', 'completada', 'pagado', 'EUR', 45000.00, 4500.00, 0.00, 40500.00, 'Sofía Fernández', 'sofia@email.com', '67890123', '+54 11 6666-6666', 'transferencia', '2024-03-05', 'Impresora Láser', 45000.00, 1, 'IMP001', true, 'Instagram', 'Sistema', 'Vendedor 1', NOW(), NOW()),

-- Ingresos de Innovación Tecnológica
(7, 'ORD-10007', '2024-03-15', 'fisico', 'completada', 'pagado', 'ARS', 25000.00, 0.00, 0.00, 25000.00, 'Roberto Silva', 'roberto@email.com', '78901234', '+54 11 7777-7777', 'efectivo', '2024-03-15', 'Disco Externo 1TB', 25000.00, 1, 'DIS001', true, 'Local', 'Sistema', 'Vendedor 2', NOW(), NOW()),
(8, 'ORD-10008', '2024-03-20', 'ecommerce', 'completada', 'pagado', 'ARS', 8000.00, 800.00, 1500.00, 8700.00, 'Carmen Vega', 'carmen@email.com', '89012345', '+54 11 8888-8888', 'mercado_pago', '2024-03-20', 'Webcam HD', 8000.00, 1, 'WEB001', true, 'Online', 'Sistema', 'Vendedor 3', NOW(), NOW()),
(9, 'ORD-10009', '2024-03-25', 'mixto', 'completada', 'pagado', 'USD', 12000.00, 1200.00, 0.00, 10800.00, 'Diego Morales', 'diego@email.com', '90123456', '+54 11 9999-9999', 'tarjeta_credito', '2024-03-25', 'Auriculares', 12000.00, 1, 'AUR001', true, 'Facebook', 'Sistema', 'Vendedor 1', NOW(), NOW()),

-- Ingresos de Software Factory
(10, 'ORD-10010', '2024-01-30', 'fisico', 'completada', 'pagado', 'ARS', 30000.00, 0.00, 0.00, 30000.00, 'Patricia Ruiz', 'patricia@email.com', '01234567', '+54 11 0000-0000', 'efectivo', '2024-01-30', 'Software Licencia', 30000.00, 1, 'SOF001', false, 'Local', 'Sistema', 'Vendedor 2', NOW(), NOW()),
(11, 'ORD-10011', '2024-02-15', 'ecommerce', 'completada', 'pagado', 'ARS', 50000.00, 5000.00, 0.00, 45000.00, 'Fernando Torres', 'fernando@email.com', '12345678', '+54 11 1111-2222', 'transferencia', '2024-02-15', 'Consultoría IT', 50000.00, 1, 'CON001', false, 'Online', 'Sistema', 'Vendedor 3', NOW(), NOW()),
(12, 'ORD-10012', '2024-03-10', 'mixto', 'completada', 'pagado', 'EUR', 15000.00, 1500.00, 0.00, 13500.00, 'Valeria Castro', 'valeria@email.com', '23456789', '+54 11 2222-3333', 'tarjeta_debito', '2024-03-10', 'Servicio de Mantenimiento', 15000.00, 1, 'SER001', false, 'WhatsApp', 'Sistema', 'Vendedor 1', NOW(), NOW()),

-- Ingresos de Data Analytics Pro
(13, 'ORD-10013', '2024-01-25', 'fisico', 'completada', 'pagado', 'ARS', 8000.00, 0.00, 0.00, 8000.00, 'Ricardo Mendez', 'ricardo@email.com', '34567890', '+54 11 3333-4444', 'efectivo', '2024-01-25', 'Reparación PC', 8000.00, 1, 'REP001', false, 'Local', 'Sistema', 'Vendedor 2', NOW(), NOW()),
(14, 'ORD-10014', '2024-02-28', 'ecommerce', 'completada', 'pagado', 'ARS', 25000.00, 2500.00, 0.00, 22500.00, 'Lucía Herrera', 'lucia@email.com', '45678901', '+54 11 4444-5555', 'mercado_pago', '2024-02-28', 'Instalación Red', 25000.00, 1, 'INS001', false, 'Online', 'Sistema', 'Vendedor 3', NOW(), NOW()),
(13, 'ORD-10015', '2024-03-18', 'mixto', 'completada', 'pagado', 'USD', 2000.00, 200.00, 0.00, 1800.00, 'Gabriel Luna', 'gabriel@email.com', '56789012', '+54 11 5555-6666', 'tarjeta_credito', '2024-03-18', 'Cable HDMI', 2000.00, 1, 'CAB001', true, 'Instagram', 'Sistema', 'Vendedor 1', NOW(), NOW());

-- Mostrar resumen de datos insertados
SELECT 'RESUMEN DE DATOS GENERADOS' as titulo;
SELECT 'Clientes' as tipo, COUNT(*) as cantidad FROM tenant_customer;
SELECT 'Unidades de Negocio' as tipo, COUNT(*) as cantidad FROM tenant_businessunit;
SELECT 'Tipos de Gasto' as tipo, COUNT(*) as cantidad FROM expenses_expensetype;
SELECT 'Gastos' as tipo, COUNT(*) as cantidad FROM expenses_expenses;
SELECT 'Ingresos' as tipo, COUNT(*) as cantidad FROM incomes_income;
SELECT 'Total Gastos' as tipo, SUM(amount) as total FROM expenses_expenses;
SELECT 'Total Ingresos' as tipo, SUM(total) as total FROM incomes_income; 