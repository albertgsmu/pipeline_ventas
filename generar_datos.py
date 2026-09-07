import pandas as pd
import random
from datetime import datetime, timedelta
import os

# Crear carpeta 'data' si no existe
if not os.path.exists('data'):
    os.makedirs('data')

random.seed(42)

# 1. PRODUCTOS
productos = pd.DataFrame({
    'producto_id': range(1, 21),
    'nombre_producto': [
        'Laptop HP', 'Mouse Logitech', 'Teclado Mecanico', 'Monitor Samsung',
        'Auriculares Sony', 'Webcam HD', 'Disco SSD 1TB', 'Memoria RAM 16GB',
        'Tablet iPad', 'Smartphone Samsung', 'Cargador USB-C', 'Cable HDMI',
        'Impresora Canon', 'Router WiFi', 'Parlante Bluetooth', 'Mousepad XL',
        'Hub USB', 'Soporte Laptop', 'Lampara LED', 'Silla Ergonomica'
    ],
    'categoria': [
        'Computadoras', 'Accesorios', 'Accesorios', 'Monitores',
        'Audio', 'Accesorios', 'Almacenamiento', 'Componentes',
        'Tablets', 'Celulares', 'Accesorios', 'Cables',
        'Impresoras', 'Redes', 'Audio', 'Accesorios',
        'Accesorios', 'Accesorios', 'Iluminacion', 'Mobiliario'
    ],
    'precio_unitario': [
        899.99, 29.99, 79.99, 349.99, 149.99, 59.99, 109.99, 89.99,
        599.99, 699.99, 19.99, 12.99, 249.99, 79.99, 49.99, 24.99,
        34.99, 44.99, 39.99, 299.99
    ]
})

# 2. CLIENTES
nombres = [
    'Carlos Garcia', 'Maria Lopez', 'Juan Martinez', 'Ana Rodriguez',
    'Pedro Sanchez', 'Laura Fernandez', 'Diego Torres', 'Carmen Ruiz',
    'Roberto Diaz', 'Sofia Morales'
]
ciudades = ['Bogota', 'Medellin', 'Cali', 'Barranquilla', 'Cartagena']

clientes = pd.DataFrame({
    'cliente_id': range(1, 11),
    'nombre_cliente': nombres,
    'email': [f"{n.split()[0].lower()}@email.com" for n in nombres],
    'ciudad': [random.choice(ciudades) for _ in range(10)],
    'fecha_registro': ['2023-01-15'] * 10
})

# 3. VENTAS (con errores intencionales para limpiar después)
n_ventas = 100
ventas_list = []

for i in range(1, n_ventas + 1):
    fecha = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 180))
    c_id = random.randint(1, 10)
    p_id = random.randint(1, 20)
    cant = random.randint(1, 5)
    precio = productos.loc[productos['producto_id'] == p_id, 'precio_unitario'].values[0]
    
    ventas_list.append({
        'venta_id': i,
        'fecha': fecha.strftime('%Y-%m-%d'),
        'cliente_id': c_id,
        'producto_id': p_id,
        'cantidad': cant,
        'precio_unitario': precio,
        'total': round(cant * precio, 2)
    })

ventas = pd.DataFrame(ventas_list)

# Insertar algunos nulos y duplicados a proposito
ventas.loc[5, 'cliente_id'] = None
ventas.loc[12, 'cantidad'] = None
ventas = pd.concat([ventas, ventas.iloc[[2, 10]]], ignore_index=True)

# Guardar a CSV
productos.to_csv('data/productos.csv', index=False)
clientes.to_csv('data/clientes.csv', index=False)
ventas.to_csv('data/ventas.csv', index=False)

print("✅ ¡Archivos CSV generados con éxito en la carpeta 'data'!")