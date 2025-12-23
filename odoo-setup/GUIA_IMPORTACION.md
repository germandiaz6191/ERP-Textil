# Guía de Importación de Datos a Odoo

Esta carpeta contiene archivos CSV precargados para acelerar tu configuración de Odoo.

## Archivos Disponibles

1. **centros_trabajo.csv** - 5 centros de trabajo estándar para textil
2. **productos_ejemplo.csv** - 3 productos de ejemplo

## Cómo Importar

### Paso 1: Importar Centros de Trabajo

1. Ir a **Manufacturing → Configuration → Work Centers**
2. Click en ⚙️ (engranaje) → **Import records**
3. Click **Upload File**
4. Seleccionar `centros_trabajo.csv`
5. Verificar que las columnas coincidan
6. Click **Import**

### Paso 2: Importar Productos

1. Ir a **Inventory → Products → Products**
2. Click en ⚙️ (engranaje) → **Import records**
3. Click **Upload File**
4. Seleccionar `productos_ejemplo.csv`
5. Verificar mapeo de columnas:
   - name → Name
   - default_code → Internal Reference
   - type → Product Type
   - list_price → Sales Price
6. Click **Test** primero (para verificar)
7. Si no hay errores, click **Import**

## Notas Importantes

- **Rutas**: El campo `route_ids/id` puede causar error si no existe
  - Solución: Marcar manualmente "Can be Manufactured" después de importar
- **Precios**: Ajusta los precios según tu realidad
- **Códigos**: Modifica los códigos internos según tu nomenclatura

## Crear Bill of Materials (BoM)

Los BoM no se pueden importar fácilmente por CSV. Se crean manualmente:

1. Ir a **Manufacturing → Products → Bills of Materials**
2. Crear para cada producto
3. Agregar operaciones con centros de trabajo y tiempos

### Ejemplo BoM: Camiseta Básica

**Components** (si los tienes):
- Tela: 1.5 metros
- Hilo: 50 metros
- Etiqueta: 1 unidad

**Operations**:
| Operation | Work Center | Duration |
|-----------|-------------|----------|
| Corte | Corte | 30 min |
| Confección | Confección | 45 min |
| Terminación | Terminación | 15 min |
| Control de Calidad | Control de Calidad | 10 min |
| Empaque | Empaque | 5 min |

## Solución de Problemas

**Error: "No matching record found"**
- Verifica que el ID externo exista
- O importa en modo "Create" en vez de "Update"

**Error de permisos**
- Asegúrate de tener permisos de administrador
- Ir a Settings → Users → Tu usuario → Access Rights

**Campos no encontrados**
- Algunos campos pueden no existir en versiones antiguas de Odoo
- Quita esas columnas del CSV

## Personalización

Puedes editar los CSVs con:
- Excel
- Google Sheets
- LibreOffice Calc
- Cualquier editor de texto

**Formato**: UTF-8, separador de coma (,)
