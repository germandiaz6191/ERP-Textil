# 🎯 Configuración Inicial - ERP Textil con Odoo

**Guía completa paso a paso** para implementar los requerimientos del cliente

⏱️ **Tiempo total:** 1-2 horas
📋 **Prerrequisito:** Odoo 17 instalado y funcionando

---

## 📋 Requerimientos del Cliente

Según el audio del cliente, el sistema debe manejar:

✅ **Referencias/Productos**
- Códigos únicos por producto
- Fichas técnicas (Bill of Materials)
- Variantes (tallas, colores)

✅ **Órdenes de Producción**
- Número consecutivo automático
- Asociar orden de compra
- Seguimiento en tiempo real

✅ **Procesos de Manufactura**
- **Corte** → **Confección** → **Terminación** → **Control de Calidad** → **Empaque**
- Asignar responsables por proceso
- Registrar tiempos estimados vs reales

✅ **Inventario**
- Traslado automático al completar producción
- Descuento automático en ventas
- Capacidad para ~50 referencias (escalable)

---

# FASE 1: Configuración Inicial (30 minutos)

## Paso 1.1: Crear Base de Datos (Si no lo hiciste)

Al acceder por primera vez a `http://TU_IP:8069`:

1. **Master Password:** La que configuraste en `config.env` (campo `ADMIN_PASSWORD`)
2. **Database Name:** `textil_erp`
3. **Email:** tu@email.com (será el usuario admin)
4. **Password:** Tu contraseña de acceso a Odoo
5. **Language:** Español (Colombia) o tu país
6. **Country:** Colombia (o tu país)
7. **Demo data:** ❌ **NO marcar**

Click **"Crear base de datos"** → Espera 2-3 minutos

---

## Paso 1.2: Activar Módulos Necesarios

Una vez dentro de Odoo:

### 1. Ir a Aplicaciones

Click en el menú superior: **"Aplicaciones"**

### 2. Activar Modo Desarrollador (Importante)

- Click en **Ajustes** (icono de engranaje arriba a la derecha)
- Baja hasta el final
- Click en **"Activar el modo de desarrollador"**

Esto te permite ver opciones avanzadas.

### 3. Instalar Módulos

Vuelve a **Aplicaciones** y busca e instala estos módulos:

**Módulos Principales:**

#### a) **Manufactura** (Manufacturing)
- Buscar: "Manufactura" o "Manufacturing"
- Click **Instalar**
- Espera 1-2 minutos

#### b) **Inventario** (Inventory)
- Buscar: "Inventario" o "Inventory"
- Click **Instalar**

#### c) **Ventas** (Sales)
- Buscar: "Ventas" o "Sales"
- Click **Instalar**

#### d) **Compra** (Purchase)
- Buscar: "Compra" o "Purchase"
- Click **Instalar**

**Módulos Opcionales (Recomendados):**

#### e) **Calidad** (Quality)
- Buscar: "Calidad" o "Quality"
- Nombre técnico debajo: `quality` o `quality_control`
- Click **Instalar**

💡 **Nota:** Los nombres pueden variar según el idioma de tu instalación.

✅ **Instalación completada** - Verás nuevos menús en la barra superior

---

## Paso 1.3: Configurar Información de la Empresa

### 1. Ir a Ajustes

Click en **Ajustes** (menú superior)

### 2. Configurar Empresa

En la sección **"Empresas"**:

- **Nombre de la empresa:** Tu Empresa Textil S.A.S.
- **Dirección:** Tu dirección
- **Teléfono:** Tu teléfono
- **Email:** contacto@tuempresa.com
- **NIT/RUT:** Tu identificación tributaria
- **Logo:** (Opcional) Sube tu logo

Click **Guardar**

### 3. Configurar Inventario (Importante)

⚠️ **IMPORTANTE:** Estas opciones están en **Ajustes** (menú superior), NO en el módulo Inventario directamente.

En **Ajustes** → Sección **"Almacén"**:

✅ Marca estas opciones:
- ☑️ **Ubicaciones de almacenamiento** (o "Ubicaciones de Almacenamiento")
- ☑️ **Rutas multietapa** (o "Rutas Multi-Paso")
- ☑️ **Categorías de almacenamiento** (Opcional)

💡 **Nota:** "Productos por Variantes" generalmente ya viene activado por defecto.

Click **Guardar** (arriba a la derecha)

### 4. Configurar Manufactura

En **Ajustes** → Sección **"Manufactura"** (o "Fabricación"):

✅ Activar:
- ☑️ **Órdenes de Trabajo** (Work Orders)
  - Al marcar esta, **Centros de Trabajo** se activa automáticamente ✅
- ☑️ **Subcontratación** (Opcional - puedes omitirlo)

Click **Guardar**

---

## Paso 1.4: Crear Centros de Trabajo

Los centros de trabajo representan cada estación/proceso en tu producción.

### 1. Ir a Manufactura → Configuración → Centros de Trabajo

**Ruta:** Manufactura → Configuración → Centros de Trabajo (o Fabricación)

### 2. Crear Centro: **CORTE**

Click **Crear**

**Pestaña "Información general":**
- **Nombre del centro de trabajo:** Corte
- **Código:** CORTE
- **Horas de trabajo:** Standard 40 hours/week (seleccionar del dropdown)

**Sección "INFORMACIÓN DE PRODUCCIÓN":**
- **Eficiencia de tiempo:** 100 %
- **Capacidad:** 1 (número simple - significa 1 operario/estación)
- **Objetivo de eficiencia general de los equipos:** 90 % (dejar por defecto)
- **Tiempo de preparación:** 00:00 minutos (o 08:00 si aplica)
- **Tiempo de limpieza:** 00:00 minutos

**Sección "INFORMACIÓN DE COSTOS":**
- **Costo por hora:** 0 (o ajusta según tu costo, ej: 10)

Click **Guardar**

### 3. Crear Centro: **CONFECCIÓN**

Click **Crear**

- **Nombre del centro de trabajo:** Confección
- **Código:** CONF
- **Horas de trabajo:** Standard 40 hours/week
- **Eficiencia de tiempo:** 100 %
- **Capacidad:** 5 (5 operarios simultáneos)
- **Tiempo de preparación:** 00:00
- **Tiempo de limpieza:** 00:00
- **Costo por hora:** 0 (o tu costo)

Click **Guardar**

### 4. Crear Centro: **TERMINACIÓN**

Click **Crear**

- **Nombre del centro de trabajo:** Terminación
- **Código:** TERM
- **Horas de trabajo:** Standard 40 hours/week
- **Eficiencia de tiempo:** 100 %
- **Capacidad:** 2
- **Tiempo de preparación:** 00:00
- **Tiempo de limpieza:** 00:00
- **Costo por hora:** 0

Click **Guardar**

### 5. Crear Centro: **CONTROL DE CALIDAD**

Click **Crear**

- **Nombre del centro de trabajo:** Control de Calidad
- **Código:** QC
- **Horas de trabajo:** Standard 40 hours/week
- **Eficiencia de tiempo:** 100 %
- **Capacidad:** 1
- **Tiempo de preparación:** 00:00
- **Tiempo de limpieza:** 00:00
- **Coste por hora:** $9.000 COP

Click **Guardar**

### 6. Crear Centro: **EMPAQUE**

Click **Crear**

- **Nombre del centro de trabajo:** Empaque
- **Código:** EMPAQ
- **Horas de trabajo:** Standard 40 hours/week
- **Eficiencia de tiempo:** 100 %
- **Capacidad:** 2
- **Tiempo de preparación:** 00:00
- **Tiempo de limpieza:** 00:00
- **Costo por hora:** 0

Click **Guardar**

✅ **Centros de Trabajo Creados** - Ahora tienes 5 centros de trabajo configurados

---

## Paso 1.5: Verificar Ubicaciones de Inventario (OPCIONAL)

> ⚠️ **ESTE PASO ES OPCIONAL** - Odoo ya trae ubicaciones por defecto suficientes para empezar.
>
> Solo necesitas crear ubicaciones adicionales si tienes necesidades específicas de organización de almacén.
>
> **Puedes saltar directamente al Paso 2.1 (Crear Categorías de Productos)** si prefieres usar la configuración por defecto.

### 1. Ir a Inventario → Configuración → Ubicaciones

**Ruta:** Inventario → Configuración → Ubicaciones

### 2. Ver TODAS las Ubicaciones (Quitar Filtros)

Por defecto, Odoo muestra un filtro "Interno" que oculta algunas ubicaciones.

**Para ver todas las ubicaciones:**
1. Busca el filtro activo cerca de la parte superior (verás algo como "Interno X")
2. Click en la **X** para quitar el filtro
3. Ahora verás la lista completa de ubicaciones

### 3. Ubicaciones que Ya Existen por Defecto

Odoo 17 ya incluye estas ubicaciones automáticamente:

**Ubicaciones Principales:**
- **WH** (Warehouse - Almacén principal)
- **WH/Existencias** (Stock - Inventario principal)
- **WH/Packing Zone** (Zona de empaque)
- **WH/Post-Production** (Post-producción)
- **WH/Pre-Production** (Pre-producción)
- **WH/Quality Control** (Control de calidad)

**Ubicaciones Virtuales:**
- **Partners** (Ubicaciones de clientes)
- **Physical Locations** (Ubicaciones físicas)
- **Virtual Locations** (Ubicaciones virtuales)

**Ubicaciones de Producción:**
- **Production** (Producción)

### 4. ¿Necesitas Crear Ubicaciones Adicionales? (OPCIONAL)

Solo crea ubicaciones adicionales si necesitas una organización más específica, por ejemplo:

**Ejemplo - Crear ubicación "Producto Terminado":**
1. Click **Crear**
2. **Nombre de Ubicación:** Producto Terminado
3. **Ubicación Principal:** WH/Existencias (seleccionar del dropdown)
4. **Tipo de Ubicación:** Ubicación interna
5. Click **Guardar**

### 💡 Recomendación:

**Para empezar, NO necesitas crear ubicaciones adicionales.** Las ubicaciones por defecto son suficientes para gestionar:
- Materias primas en WH/Existencias
- Producción en WH/Pre-Production y Production
- Control de calidad en WH/Quality Control
- Producto terminado en WH/Post-Production
- Empaque en WH/Packing Zone

✅ **Ubicaciones Verificadas** - Puedes continuar con el siguiente paso

---

# FASE 2: Productos y Bill of Materials (45 minutos)

## Paso 2.1: Crear Categorías de Productos

### 1. Ir a Inventario → Configuración → Categorías de Productos

**Ruta:** Inventario → Configuración → Categorías de Productos

Verás las categorías por defecto:
- All
- All / Expenses
- All / Saleable

### 2. Crear Categoría: **Producto Terminado**

Click **Nuevo** (arriba a la izquierda)

**Campos a llenar:**

**Categoría:**
- **Nombre:** `Producto Terminado`
- **Categoría principal:** Dejar vacío o "All" (valor por defecto)

**VALUACIÓN DE INVENTARIO:**
- **Método de coste:** `Costo promedio (AVCO)`

**LOGÍSTICA:**
- **Rutas:** Dejar vacío
- **Estrategia de remoción forzada:** Dejar vacío o seleccionar `Primeras entradas, primeras salidas (PEPS)`

Click **Guardar**

### 3. Crear Categoría: **Materia Prima**

Click **Nuevo**

**Campos a llenar:**

**Categoría:**
- **Nombre:** `Materia Prima`
- **Categoría principal:** Dejar vacío o "All"

**VALUACIÓN DE INVENTARIO:**
- **Método de coste:** `Costo promedio (AVCO)`

Click **Guardar**

### 4. Crear Categoría: **Insumos**

Click **Nuevo**

**Campos a llenar:**

**Categoría:**
- **Nombre:** `Insumos`
- **Categoría principal:** Dejar vacío o "All"

**VALUACIÓN DE INVENTARIO:**
- **Método de coste:** `Costo promedio (AVCO)`

Click **Guardar**

### 5. Verificar Categorías Creadas

En la lista de **Categorías de productos** deberías ver ahora:
- All
- All / Expenses
- All / Saleable
- **Producto Terminado** ✅
- **Materia Prima** ✅
- **Insumos** ✅

✅ **Categorías de Productos Creadas**

---

## Paso 2.2: Crear Atributos de Producto (Variantes)

Para manejar tallas y colores.

### 1. Ir a Inventario → Configuración → Atributos

**Ruta:** Inventario → Configuración → Atributos

### 2. Crear Atributo: **TALLA**

Click **Nuevo** (arriba a la izquierda)

**Configuración:**
- **Nombre del atributo:** `Talla`
- **Tipo de visualización:** Seleccionar `Seleccionar` (radio button)
- **Modo de creación de las variantes:** Seleccionar `Instantánea` (radio button)

**Valores del atributo:**

En la tabla, click **Agregar una línea** para cada talla:

| Valor | Es val... | Precio ad... |
|-------|-----------|--------------|
| XS    | ⬜        | 0,00         |
| S     | ⬜        | 0,00         |
| M     | ⬜        | 0,00         |
| L     | ⬜        | 0,00         |
| XL    | ⬜        | 0,00         |
| XXL   | ⬜        | 0,00         |

> 💡 Solo escribe el **Valor** (la talla), los demás campos déjalos por defecto

Click **Guardar**

### 3. Crear Atributo: **COLOR**

Click **Nuevo**

**Configuración:**
- **Nombre del atributo:** `Color`
- **Tipo de visualización:** Seleccionar `Color` (radio button) ← Usaremos tipo Color para este atributo
- **Modo de creación de las variantes:** Seleccionar `Instantánea` (radio button)

**Valores del atributo:**

Click **Agregar una línea** para cada color:

| Valor  | Es val... | Precio ad... |
|--------|-----------|--------------|
| Blanco | ⬜        | 0,00         |
| Negro  | ⬜        | 0,00         |
| Azul   | ⬜        | 0,00         |
| Rojo   | ⬜        | 0,00         |
| Verde  | ⬜        | 0,00         |
| Gris   | ⬜        | 0,00         |

> 💡 Si usas tipo "Color", podrás seleccionar un color visual para cada valor

Click **Guardar**

✅ **Atributos de Producto Creados** - Talla y Color configurados para crear variantes

---

## Paso 2.3: Crear Materias Primas

### 1. Ir a Inventario → Productos → Productos

**Ruta:** Inventario → Productos → Productos

Click **Nuevo** (arriba a la izquierda)

---

#### Producto 1: **Tela de Algodón**

**PESTAÑA: Información general**

**Campos básicos:**
- **Nombre del producto:** `Tela de Algodón`
- Checkboxes:
  - ⬜ **Se puede vender** (NO marcar)
  - ☑️ **Se puede comprar** (Marcar)

**Campos adicionales:**
- **Tipo de producto:** `Producto almacenable` (seleccionar del dropdown)
- **Categoría del producto:** `All / Materia Prima`

**PESTAÑA: Compras**

En la tabla de proveedores, click **Agregar una línea**:

| Proveedor | Cantidad | Precio | Divisa |
|-----------|----------|--------|--------|
| (opcional - puedes dejarlo vacío o crear uno) | `1` | `15000` | `COP` |

> 💡 **Nota sobre "Cantidad":** Este campo es la **cantidad mínima de compra**, no la unidad de medida. Pon `1` para indicar que el precio aplica desde 1 unidad en adelante.

> 💡 **Nota sobre Unidad de Medida:** En Odoo 17, la unidad de medida por defecto es "Unidades". Para tela vendida por metro, el sistema lo trata internamente como unidades, y el precio $15.000 se entiende como "por metro".

**PESTAÑA: Inventario**

En la sección **OPERACIONES:**
- ☑️ **Comprar** (debe estar marcado)
- ⬜ Fabricar (dejar sin marcar)

**Guardar** el producto

---

#### Producto 2: **Hilo de Coser**

Click **Nuevo**

**PESTAÑA: Información general**
- **Nombre del producto:** `Hilo de Coser`
- ⬜ **Se puede vender**
- ☑️ **Se puede comprar**
- **Tipo de producto:** `Producto almacenable`
- **Categoría del producto:** `All / Insumos`

**PESTAÑA: Compras**

Click **Agregar una línea**:

| Proveedor | Cantidad | Precio | Divisa |
|-----------|----------|--------|--------|
| (vacío) | `1` | `2000` | `COP` |

**PESTAÑA: Inventario**
- ☑️ **Comprar**

**Guardar**

---

#### Producto 3: **Botones**

Click **Nuevo**

**PESTAÑA: Información general**
- **Nombre del producto:** `Botones`
- ⬜ **Se puede vender**
- ☑️ **Se puede comprar**
- **Tipo de producto:** `Producto almacenable`
- **Categoría del producto:** `All / Insumos`

**PESTAÑA: Compras**

Click **Agregar una línea**:

| Proveedor | Cantidad | Precio | Divisa |
|-----------|----------|--------|--------|
| (vacío) | `1` | `500` | `COP` |

**PESTAÑA: Inventario**
- ☑️ **Comprar**

**Guardar**

---

#### Producto 4: **Etiquetas**

Click **Nuevo**

**PESTAÑA: Información general**
- **Nombre del producto:** `Etiquetas`
- ⬜ **Se puede vender**
- ☑️ **Se puede comprar**
- **Tipo de producto:** `Producto almacenable`
- **Categoría del producto:** `All / Insumos`

**PESTAÑA: Compras**

Click **Agregar una línea**:

| Proveedor | Cantidad | Precio | Divisa |
|-----------|----------|--------|--------|
| (vacío) | `1` | `200` | `COP` |

**PESTAÑA: Inventario**
- ☑️ **Comprar**

**Guardar**

---

✅ **Materias Primas e Insumos Creados:**
- Tela de Algodón (Materia Prima) - $15.000 COP
- Hilo de Coser (Insumo) - $2.000 COP
- Botones (Insumo) - $500 COP
- Etiquetas (Insumo) - $200 COP

---

## Paso 2.4: Crear Producto Terminado con Variantes

### 1. Ir a Inventario → Productos → Productos

**Ruta:** Inventario → Productos → Productos

Click **Nuevo** (arriba a la izquierda)

---

### 2. Crear Producto: **Camiseta Básica**

**PESTAÑA: Información general**

**Campos básicos:**
- **Nombre del producto:** `Camiseta Básica`
- Checkboxes:
  - ☑️ **Se puede vender** (Marcar - este es un producto para venta)
  - ⬜ **Se puede comprar** (NO marcar - lo fabricamos, no lo compramos)

**Campos adicionales:**
- **Tipo de producto:** `Producto almacenable`
- **Política de facturación:** Dejar como está (Cantidad ordenada)
- **Precio de venta:** `35000` (o el precio que desees)
- **Categoría del producto:** `All / Producto Terminado`

---

### 3. Agregar Variantes (Tallas y Colores)

**PESTAÑA: Atributos y variantes**

Click en la pestaña **"Atributos y variantes"**

**Agregar atributo TALLA:**

1. Click **Agregar una línea** en la tabla de atributos

**En la línea que aparece:**
- **Atributo:** Selecciona `Talla` (del dropdown)
- **Valores:** Click en el campo y selecciona las tallas que quieres:
  - ☑️ S
  - ☑️ M
  - ☑️ L
  - ☑️ XL

> 💡 Puedes seleccionar múltiples valores haciendo click en cada uno

**Agregar atributo COLOR:**

2. Click **Agregar una línea** nuevamente

**En la segunda línea:**
- **Atributo:** Selecciona `Color` (del dropdown)
- **Valores:** Selecciona los colores que quieres:
  - ☑️ Blanco
  - ☑️ Negro
  - ☑️ Azul

---

### 4. Verificar Generación de Variantes

Odoo generará automáticamente **12 variantes** (4 tallas × 3 colores):
- Camiseta Básica (S, Blanco)
- Camiseta Básica (S, Negro)
- Camiseta Básica (S, Azul)
- Camiseta Básica (M, Blanco)
- Camiseta Básica (M, Negro)
- Camiseta Básica (M, Azul)
- Camiseta Básica (L, Blanco)
- Camiseta Básica (L, Negro)
- Camiseta Básica (L, Azul)
- Camiseta Básica (XL, Blanco)
- Camiseta Básica (XL, Negro)
- Camiseta Básica (XL, Azul)

---

### 5. Configurar Inventario

**PESTAÑA: Inventario**

En la sección **OPERACIONES:**
- ⬜ Comprar (NO marcar - no se compra)
- ☑️ **Fabricar** (Marcar - se manufactura)

---

### 6. Guardar el Producto

Click **Guardar**

✅ **Producto Terminado con Variantes Creado**

El producto "Camiseta Básica" ahora tiene 12 variantes diferentes que se pueden fabricar y vender.

---

## Paso 2.5: Crear Bill of Materials (BoM)

La ficha técnica de producción.

### 1. Ir a Manufactura → Productos → Lista de Materiales

**Ruta:** Manufactura → Productos → Lista de Materiales

Click **Nuevo**

### 2. Configurar BoM: **Camiseta Básica**

**Información General:**
- **Producto:** Camiseta Básica (selecciona del listado)
- **Cantidad:** 1 Unidad
- **Tipo de BoM:** Fabricar este producto
- **Referencia:** BOM-CAM-001

### 3. Agregar Componentes (Materias Primas)

En la pestaña **"Componentes"**:

Click **Agregar una línea** para cada componente:

| Componente | Cantidad | Unidad |
|------------|----------|--------|
| Tela de Algodón | 1.5 | Metros |
| Hilo de Coser | 1 | Unidades |
| Botones | 4 | Unidades |
| Etiquetas | 1 | Unidades |

### 4. Agregar Operaciones (Procesos)

En la pestaña **"Operaciones"**:

Click **Agregar una línea** para cada operación:

#### Operación 1: CORTE
- **Centro de Trabajo:** Corte
- **Nombre de la Operación:** Corte de Tela
- **Duración Predeterminada:** 15 minutos
- **Instrucciones de Trabajo:** "Cortar tela según patrón de talla"

#### Operación 2: CONFECCIÓN
- **Centro de Trabajo:** Confección
- **Nombre de la Operación:** Costura
- **Duración Predeterminada:** 45 minutos
- **Instrucciones:** "Coser piezas, ensamblar camiseta"

#### Operación 3: TERMINACIÓN
- **Centro de Trabajo:** Terminación
- **Nombre de la Operación:** Terminación
- **Duración Predeterminada:** 20 minutos
- **Instrucciones:** "Aplicar botones, etiquetas, planchado"

#### Operación 4: CONTROL DE CALIDAD
- **Centro de Trabajo:** Control de Calidad
- **Nombre de la Operación:** Inspección QC
- **Duración Predeterminada:** 10 minutos
- **Instrucciones:** "Verificar costuras, medidas, acabados"

#### Operación 5: EMPAQUE
- **Centro de Trabajo:** Empaque
- **Nombre de la Operación:** Empaque Final
- **Duración Predeterminada:** 5 minutos
- **Instrucciones:** "Empacar en bolsa, etiquetar para venta"

Click **Guardar**

✅ **Bill of Materials Completo**

**Resumen:**
- Producto: Camiseta Básica
- Componentes: 4 materias primas
- Operaciones: 5 procesos (Corte → Confección → Terminación → QC → Empaque)
- Tiempo total estimado: 95 minutos por unidad

---

# FASE 3: Primera Orden de Producción (20 minutos)

## Paso 3.1: Verificar Inventario de Materias Primas

Antes de producir, necesitamos tener materias primas en inventario.

### 1. Ir a Inventario → Productos → Productos

Busca **"Tela de Algodón"**

### 2. Actualizar Cantidad en Mano

Click en el producto → Pestaña **"Inventario"**

Click en **"Actualizar Cantidad"**

- **Ubicación:** WH/Stock
- **Cantidad:** 100 metros

Click **Aplicar**

### 3. Repetir para todos los componentes:

- **Hilo de Coser:** 50 unidades
- **Botones:** 200 unidades
- **Etiquetas:** 100 unidades

✅ **Inventario Cargado**

---

## Paso 3.2: Crear Orden de Producción

### 1. Ir a Manufactura → Operaciones → Órdenes de fabricación

**Ruta:** Manufactura → Operaciones → Órdenes de fabricación

Click **Nuevo**

### 2. Configurar Orden de Producción

**Campos principales:**
- **Producto:** Camiseta Básica (M, Blanco) - Selecciona una variante específica
- **Cantidad:** 10,00 unidades
- **Lista de materiales:** Camiseta Básica (se selecciona automáticamente)
- **Fecha programada:** Se genera automáticamente (puedes modificarla)

**PESTAÑA: Misceláneo (Opcional)**

Si quieres rastrear el origen de esta orden:
- **Origen:** OC-2024-001 (referencia a orden de compra del cliente, pedido, etc.)
- **Fecha Planificada:** Hoy

Click **Confirmar**

✅ Odoo generará automáticamente:
- **Número de orden consecutivo**: MO/00001
- **5 Órdenes de Trabajo** (una por cada operación)
- **Reserva de materiales** del inventario

---

## Paso 3.3: Ejecutar Órdenes de Trabajo

### 1. Ver Órdenes de Trabajo

En la Orden de Producción, click en la pestaña **"Órdenes de Trabajo"**

Verás 5 órdenes:
1. Corte de Tela (15 min estimados)
2. Costura (45 min estimados)
3. Terminación (20 min estimados)
4. Inspección QC (10 min estimados)
5. Empaque Final (5 min estimados)

### 2. Acceder a las Órdenes de Trabajo

Después de confirmar la orden de producción, Odoo genera automáticamente **5 órdenes de trabajo** (una por cada operación del BoM).

**Cómo acceder:**
- **Desde la Orden de Producción:** Click en la pestaña **"Órdenes de trabajo"**
- **O desde el menú:** Manufactura → Operaciones → Órdenes de trabajo

Verás las 5 órdenes:
1. Corte de Tela (15 min estimados)
2. Costura/Confección (45 min estimados)
3. Terminación (20 min estimados)
4. Inspección QC (10 min estimados)
5. Empaque Final (5 min estimados)

---

### 3. Ejecutar Operación 1: CORTE DE TELA

Click en la orden de trabajo **"Corte de Tela"** (aparecerá como 1/5 arriba)

**Estados de la orden:**
- 🔘 En espera de otra orden de trabajo
- 🔘 En espera de los componentes
- 🔘 Disponible
- 🔘 **En progreso** ← Selecciona este
- 🔘 Terminada

**Paso a paso:**

1. **Iniciar la orden:**
   - Click en el botón **"En progreso"** (arriba)
   - Esto inicia el seguimiento de tiempo automáticamente

2. **Pestaña "Seguimiento de tiempo":**
   - Verás una tabla que registra automáticamente:
     - Usuario (quien inició la orden)
     - Duración
     - Fecha de inicio
     - Fecha de finalización
   - El sistema registra el tiempo real trabajado

3. **Simular trabajo:** (opcional para pruebas)
   - Espera unos segundos/minutos simulando el trabajo de corte
   - O continúa inmediatamente al siguiente paso

4. **Finalizar la operación:**
   - Click en el botón **"Terminada"** (arriba a la derecha)
   - Odoo registra el **tiempo real** vs **tiempo estimado** (15 min)

✅ Operación 1 completada

**Navegación:**
- Usa las **flechas ← →** junto a "1 / 5" para moverte entre órdenes de trabajo

---

### 4. Ejecutar Operación 2: CONFECCIÓN

Click en la flecha **→** para ir a la orden 2/5 o búscala en la lista de órdenes de trabajo.

**Orden: Costura/Confección**

1. Click **"En progreso"**
2. (Simular trabajo de costura)
3. Click **"Terminada"**

✅ Operación 2 completada

---

### 5. Ejecutar Operaciones Restantes

Repite el mismo proceso para las órdenes 3/5, 4/5, 5/5:

**Orden 3/5: Terminación**
- Click "En progreso" → Trabajar → Click "Terminada"

**Orden 4/5: Inspección QC**
- Click "En progreso" → Trabajar → Click "Terminada"

**Orden 5/5: Empaque Final**
- Click "En progreso" → Trabajar → Click "Terminada"

✅ **Todas las órdenes de trabajo completadas** (5/5)

> 💡 **Nota sobre usuarios:** No necesitas crear usuarios específicos (cortador, costurera, etc.) para hacer pruebas. El sistema registra automáticamente quién trabaja en cada orden. Si en el futuro quieres separar por operador, puedes crear usuarios adicionales en Ajustes → Usuarios.

---

## Paso 3.4: Completar Producción

### 1. Volver a la Orden de Producción

Click en **MO/00001**

### 2. Producir

Click en **"Producir Todo"**

Odoo:
- ✅ Descuenta materias primas del inventario
- ✅ Agrega 10 unidades de "Camiseta Básica (M, Blanco)" al inventario
- ✅ Traslada automáticamente a la ubicación **WH/Stock/Producto Terminado**

Estado: **Hecho** ✅

---

## Paso 3.5: Verificar Inventario

### 1. Ir a Inventario → Productos → Productos

Busca **"Camiseta Básica (M, Blanco)"**

### 2. Ver Cantidad en Mano

Deberías ver:
- **Cantidad en Mano:** 10 unidades
- **Ubicación:** WH/Stock/Producto Terminado

✅ **Producción completada y en inventario**

---

# FASE 4: Venta y Descuento Automático (15 minutos)

## Paso 4.1: Crear Cliente

### 1. Ir a Ventas → Órdenes → Clientes

Click **Crear**

- **Nombre:** Distribuidora Moda S.A.S.
- **Email:** ventas@distribuidoramoda.com
- **Teléfono:** +57 300 123 4567
- **NIT:** 900.123.456-7

Click **Guardar**

---

## Paso 4.2: Crear Orden de Venta

### 1. Ir a Ventas → Órdenes → Presupuestos

Click **Crear**

### 2. Configurar Orden de Venta

**Información:**
- **Cliente:** Distribuidora Moda S.A.S.
- **Fecha de Validez:** 15 días desde hoy

**Líneas del Presupuesto:**

Click **Agregar un producto**

- **Producto:** Camiseta Básica (M, Blanco)
- **Cantidad:** 5 unidades
- **Precio Unitario:** $35.000 COP (se llena automáticamente)

**Total:** $175.000 COP

Click **Confirmar**

✅ Odoo genera automáticamente:
- **Número de orden:** SO001
- **Orden de entrega** (Delivery Order)

---

## Paso 4.3: Procesar Entrega

### 1. Click en el botón **"Entrega"** (arriba)

Te lleva a la Orden de Entrega.

### 2. Validar Disponibilidad

Verás:
- **Producto:** Camiseta Básica (M, Blanco)
- **Demanda:** 5 unidades
- **Reservado:** 5 unidades ✅

(Las 5 unidades se reservaron automáticamente del inventario)

### 3. Validar Entrega

Click **"Validar"**

Odoo:
- ✅ **Descuenta automáticamente** 5 unidades del inventario
- ✅ Cambia estado a **Hecho**

---

## Paso 4.4: Verificar Inventario

### 1. Ir a Inventario → Productos → Productos

Busca **"Camiseta Básica (M, Blanco)"**

### 2. Ver Cantidad Actualizada

Deberías ver:
- **Cantidad en Mano:** 5 unidades (antes: 10, vendidas: 5)
- **Cantidad Prevista:** 5 unidades

✅ **Descuento automático funcionando**

---

# ✅ Configuración Completada

## 🎉 ¡Felicitaciones! Has implementado:

### ✅ Módulos Activados:
- Manufacturing (Fabricación)
- Inventory (Inventario)
- Sales (Ventas)
- Purchase (Compras)
- Quality (Control de Calidad)

### ✅ Centros de Trabajo Configurados:
- Corte
- Confección
- Terminación
- Control de Calidad
- Empaque

### ✅ Productos Creados:
- Producto Terminado: Camiseta Básica (12 variantes)
- Materias Primas: Tela, Hilo, Botones, Etiquetas

### ✅ Bill of Materials (BoM):
- Componentes definidos
- 5 Operaciones configuradas con tiempos

### ✅ Flujo Completo Probado:
- ✅ Orden de Producción creada (MO/00001)
- ✅ Órdenes de trabajo ejecutadas
- ✅ Responsables asignados
- ✅ Tiempos registrados
- ✅ Producción completada
- ✅ Inventario actualizado automáticamente
- ✅ Venta realizada
- ✅ Descuento automático de inventario

---

# 📚 Próximos Pasos

## 1. Agregar Más Productos

Repite el proceso de Paso 2.4 y 2.5 para crear:
- Pantalones
- Camisas
- Vestidos
- etc.

Hasta completar tus ~50 referencias.

## 2. Importar Datos Masivamente

Para crear múltiples productos rápidamente:

**Ruta:** Inventario → Configuración → Importar Registros

Puedes importar productos desde CSV/Excel.

**Ejemplo de CSV:**
```csv
Nombre,Código,Precio Venta,Categoría,Tipo
Camiseta Polo,CAM-POLO,45000,Producto Terminado,Almacenable
Pantalón Jean,PANT-JEAN,75000,Producto Terminado,Almacenable
```

## 3. Configurar Usuarios y Permisos

**Ruta:** Ajustes → Usuarios y Empresas → Usuarios

Crea usuarios para:
- Operarios (solo ver y ejecutar órdenes de trabajo)
- Supervisores (crear órdenes de producción)
- Administradores (acceso completo)

## 4. Configurar Reportes

**Ruta:** Fabricación → Reportes

- **Eficiencia de Centros de Trabajo**
- **Tiempo Real vs Estimado**
- **Productividad por Operario**

## 5. Integrar Compras

Cuando el inventario de materias primas baje:

**Ruta:** Compras → Órdenes → Solicitudes de Presupuesto

- Crear orden de compra
- Asociar con proveedor
- Recibir materiales
- Actualizar inventario automáticamente

## 6. Configurar Clientes Recurrentes

**Ruta:** Ventas → Configuración → Clientes

Agregar tus clientes principales con:
- Precios especiales
- Descuentos
- Términos de pago

---

# 🔧 Personalización Adicional

## Números Consecutivos Personalizados

Si quieres cambiar el formato de los números de orden:

**Ruta:** Ajustes → Técnico → Secuencias

Busca "Orden de Fabricación" y edita el formato:
- Prefijo: `MO/%(year)s/`
- Resultado: `MO/2024/00001`

## Campos Personalizados

Para agregar campos adicionales (ej: "Orden de Compra del Cliente"):

**Ruta:** Ajustes → Técnico → Modelos

- Busca "Orden de Fabricación"
- Agrega campo personalizado

## Automatizaciones

**Ruta:** Ajustes → Técnico → Automatización

Crear automatizaciones como:
- Enviar email cuando orden de producción esté lista
- Notificar cuando inventario esté bajo
- Generar orden de compra automáticamente

---

# 📞 Soporte

## Documentación Oficial Odoo:
- [Manufacturing](https://www.odoo.com/documentation/17.0/applications/inventory_and_mrp/manufacturing.html)
- [Inventory](https://www.odoo.com/documentation/17.0/applications/inventory_and_mrp/inventory.html)
- [Sales](https://www.odoo.com/documentation/17.0/applications/sales.html)

## Comunidad Odoo:
- [Foro Oficial](https://www.odoo.com/forum)
- [YouTube Tutorials](https://youtube.com/results?search_query=odoo+17+manufacturing+tutorial)

## Archivos de este Proyecto:
- `FLUJO_TRABAJO_TEXTIL.md` - Flujo detallado de manufactura textil
- `GUIA_IMPORTACION.md` - Cómo importar datos masivamente
- `deployment/README.md` - Mantenimiento del servidor

---

# ✅ Checklist de Configuración

- [ ] Base de datos creada
- [ ] Módulos instalados (Manufacturing, Inventory, Sales, Purchase, Quality)
- [ ] Información de empresa configurada
- [ ] 5 Centros de trabajo creados
- [ ] Ubicaciones de inventario verificadas
- [ ] Categorías de productos creadas
- [ ] Atributos de variantes creados (Talla, Color)
- [ ] Materias primas creadas (4 componentes)
- [ ] Producto terminado creado con variantes
- [ ] Bill of Materials (BoM) creado con 5 operaciones
- [ ] Inventario de materias primas cargado
- [ ] Primera orden de producción completada
- [ ] Órdenes de trabajo ejecutadas
- [ ] Producto en inventario verificado
- [ ] Orden de venta procesada
- [ ] Descuento automático de inventario verificado

---

**¡Tu ERP Textil está listo para producción!** 🎉

Ahora puedes empezar a crear tus productos reales, configurar tus procesos específicos y gestionar tu producción textil de forma profesional.
