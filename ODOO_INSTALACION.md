# Guía de Instalación y Configuración de Odoo para Producción Textil

## Paso 1: Instalación de Odoo

### Opción A: Docker (Recomendado - Más Fácil)

```bash
# 1. Instalar Docker (si no lo tienes)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 2. Crear directorio para Odoo
mkdir ~/odoo-textil
cd ~/odoo-textil

# 3. Copiar el docker-compose.yml de este repositorio
cp docker-compose.yml ~/odoo-textil/

# 4. Iniciar Odoo
docker-compose up -d

# 5. Esperar 1-2 minutos y abrir: http://localhost:8069
```

**Credenciales:**
- Master Password: `admin123`
- Crear base de datos: `textil_erp`
- Email: tu email
- Password: la que quieras

### Opción B: Instalación Nativa (Ubuntu/Debian)

```bash
# 1. Instalar PostgreSQL
sudo apt update
sudo apt install postgresql -y

# 2. Crear usuario de base de datos
sudo su - postgres -c "createuser -s $USER"

# 3. Instalar dependencias
sudo apt install python3-pip python3-dev libxml2-dev libxslt1-dev \
  libldap2-dev libsasl2-dev libtiff5-dev libjpeg8-dev libopenjp2-7-dev \
  zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev libharfbuzz-dev \
  libfribidi-dev libxcb1-dev libpq-dev git node-less npm -y

# 4. Descargar Odoo
cd ~
git clone https://github.com/odoo/odoo --depth 1 --branch 17.0
cd odoo

# 5. Instalar dependencias Python
pip3 install -r requirements.txt

# 6. Crear archivo de configuración
cat > odoo.conf <<EOF
[options]
admin_passwd = admin123
db_host = localhost
db_port = 5432
db_user = $USER
addons_path = addons
xmlrpc_port = 8069
EOF

# 7. Iniciar Odoo
./odoo-bin -c odoo.conf
```

Abrir: http://localhost:8069

---

## Paso 2: Configuración Inicial

### 2.1 Crear Base de Datos

1. En http://localhost:8069 verás pantalla de creación de BD
2. Master Password: `admin123`
3. Database Name: `textil_erp`
4. Email: tu email
5. Password: tu contraseña
6. Language: Spanish
7. Country: Colombia (o tu país)
8. Click "Create database"

### 2.2 Instalar Módulos Necesarios

Una vez dentro de Odoo:

1. **Ir a Apps** (menú superior)
2. **Quitar filtro "Apps"** (para ver todos los módulos)
3. **Instalar estos módulos en orden:**

#### Módulos Básicos:
- ✅ **Inventory** (Inventario) - Gestión de stock
- ✅ **Manufacturing** (Fabricación/MRP) - Órdenes de producción
- ✅ **Sales** (Ventas) - Para gestionar ventas y clientes
- ✅ **Purchase** (Compras) - Para órdenes de compra

#### Módulos Opcionales (recomendados):
- **Quality** - Control de calidad
- **Maintenance** - Mantenimiento de equipos
- **Barcode** - Escaneo de códigos de barras
- **Project** - Si quieres gestionar proyectos

**Importante**: Al instalar Manufacturing, automáticamente se instalan dependencias necesarias.

---

## Paso 3: Configuración para Producción Textil

### 3.1 Configurar Centros de Trabajo (Workcenter)

Los centros de trabajo son las estaciones donde se realizan los procesos.

**Ir a: Manufacturing → Configuration → Work Centers**

Crear estos centros de trabajo:

1. **Centro de Corte**
   - Name: Corte
   - Working Hours: 8 horas/día
   - Time Efficiency: 100%
   - Capacity: 1

2. **Centro de Confección**
   - Name: Confección
   - Working Hours: 8 horas/día
   - Capacity: 5 (si tienes 5 máquinas)

3. **Centro de Terminación**
   - Name: Terminación/Acabado
   - Working Hours: 8 horas/día

4. **Control de Calidad**
   - Name: Control de Calidad
   - Working Hours: 8 horas/día

5. **Centro de Empaque**
   - Name: Empaque
   - Working Hours: 8 horas/día

### 3.2 Crear Productos (Referencias)

**Ir a: Inventory → Products → Products**

**Ejemplo: Camiseta Básica**

1. Click "Create"
2. **General Information:**
   - Product Name: Camiseta Básica Blanca
   - Internal Reference: CAM-BAS-001
   - Product Type: Storable Product
   - ✅ Can be Manufactured

3. **Sales tab:**
   - Sales Price: precio de venta

4. **Inventory tab:**
   - Routes: ✅ Manufacture

### 3.3 Crear Bill of Materials (BoM) - Lista de Materiales

**Ir a: Manufacturing → Products → Bills of Materials**

Para cada producto, crear su BoM:

**Ejemplo: BoM para Camiseta**

1. Click "Create"
2. **Product**: Camiseta Básica Blanca
3. **Quantity**: 1
4. **Components** (materiales necesarios):
   - Tela blanca: 1.5 metros
   - Hilo: 50 metros
   - Etiqueta: 1 unidad
   - Botones: 3 unidades (si aplica)

5. **Operations** (Procesos/Operaciones):

   Click "Add a line" en la pestaña Operations:

   | Operation | Work Center | Duration (min) |
   |-----------|-------------|----------------|
   | Corte de tela | Corte | 30 |
   | Confección | Confección | 45 |
   | Terminación | Terminación | 15 |
   | Control de Calidad | Control de Calidad | 10 |
   | Empaque | Empaque | 5 |

6. **Guardar**

---

## Paso 4: Crear Orden de Producción

### 4.1 Crear Manufacturing Order

**Ir a: Manufacturing → Operations → Manufacturing Orders**

1. Click "Create"
2. **Product**: Seleccionar tu producto
3. **Quantity**: cantidad a producir
4. **Reference**: número de orden (ej: OP-001)
5. **Scheduled Date**: fecha programada
6. **Source Document**: orden de compra del cliente (opcional)

7. Click "Confirm"

### 4.2 Asignar Responsables

Para cada operación en la orden:

1. Abrir la orden
2. En la pestaña "Work Orders" verás todas las operaciones
3. Click en cada operación
4. Asignar **Responsible**: nombre del operario/responsable
5. Iniciar trabajo: Click "Start"
6. Al terminar: Click "Mark as Done"

### 4.3 Completar Orden

Cuando todas las operaciones estén completadas:
- Click "Produce" (botón verde)
- El producto se agrega automáticamente al inventario

---

## Paso 5: Gestión de Inventario

### 5.1 Ver Inventario

**Ir a: Inventory → Reporting → Inventory Report**

Aquí ves todo tu inventario disponible por producto.

### 5.2 Ajustes Manuales

**Ir a: Inventory → Operations → Inventory Adjustments**

Para ajustar cantidades manualmente:
1. Click "Create"
2. Seleccionar producto
3. Cantidad actual vs nueva cantidad
4. Click "Apply"

### 5.3 Movimientos

**Ir a: Inventory → Reporting → Moves History**

Historial completo de todos los movimientos de inventario.

---

## Paso 6: Reportes y Seguimiento

### 6.1 Dashboard de Manufactura

**Manufacturing → Manufacturing Orders**

Vista de todas las órdenes:
- Por estado (Draft, Confirmed, Progress, Done)
- Progreso de cada orden
- Órdenes atrasadas (en rojo)

### 6.2 Análisis de Tiempos

**Manufacturing → Reporting → Work Orders**

- Tiempos estimados vs reales
- Eficiencia por centro de trabajo
- Operarios más productivos

### 6.3 Inventario en Tiempo Real

**Inventory → Reporting → Inventory Valuation**

- Valor total del inventario
- Stock por ubicación
- Productos bajo stock mínimo

---

## Paso 7: Configuraciones Avanzadas

### 7.1 Rutas de Fabricación Alternativas

Si un producto se puede fabricar de diferentes maneras:
- Crear múltiples BoMs para el mismo producto
- Marcar diferentes rutas en "Routing"

### 7.2 Variantes de Producto

Para tallas, colores, etc:

**Ir a: Settings → General Settings → Products**
- ✅ Enable "Product Variants"

Luego en cada producto:
- Crear atributos (Talla: S, M, L, XL)
- Crear atributos (Color: Blanco, Negro, Azul)
- Odoo genera automáticamente todas las combinaciones

### 7.3 Control de Calidad

**Instalar módulo Quality**

Crear puntos de control:
- Después de corte
- Después de confección
- Antes de empaque

---

## Mapeo: Mi Sistema → Odoo

| Mi Desarrollo | Odoo MRP |
|---------------|----------|
| Referencias | Products (con "Can be Manufactured") |
| Orden de Producción | Manufacturing Order |
| Procesos | Operations en BoM |
| Centros de Trabajo | Work Centers |
| Responsable de proceso | Responsible en Work Order |
| Tiempos estimados | Duration en Operations |
| Tiempos reales | Real Duration (auto-calculado) |
| Traslado a inventario | Automático al hacer "Produce" |
| Movimientos de inventario | Stock Moves (automático) |
| Dashboard | Manufacturing Dashboard |

---

## Tips y Mejores Prácticas

1. **Empezar Simple**: Crea 2-3 productos primero, prueba el flujo completo
2. **Documentar Procesos**: Usa el campo "Notes" para guardar detalles
3. **Códigos Consistentes**: Usa prefijos (CAM-, PAN-, etc.)
4. **Backups**: Hacer backup regular de la base de datos
5. **Usuarios**: Crear usuarios para cada responsable con permisos específicos

---

## Soporte y Recursos

- **Documentación Oficial**: https://www.odoo.com/documentation/17.0/
- **Foro Comunidad**: https://www.odoo.com/forum
- **YouTube**: "Odoo Manufacturing Tutorial" (muchos videos)
- **Odoo eLearning**: Cursos gratuitos en https://www.odoo.com/slides

---

## Próximos Pasos

1. ✅ Instalar Odoo siguiendo Paso 1
2. ✅ Configurar módulos (Paso 2)
3. ✅ Crear centros de trabajo (Paso 3.1)
4. ✅ Crear 1 producto de prueba (Paso 3.2)
5. ✅ Crear su BoM (Paso 3.3)
6. ✅ Crear orden de producción de prueba (Paso 4)
7. ✅ Completar el flujo completo
8. ✅ Replicar para más productos

**Tiempo estimado de setup**: 2-4 horas para configuración inicial completa.
