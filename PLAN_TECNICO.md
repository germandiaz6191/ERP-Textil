# Plan Técnico - Sistema ERP Textil

## Resumen de Requisitos

El cliente necesita un sistema para gestionar órdenes de producción textil con:
- Gestión de órdenes de producción con procesos (corte, confección, etc.)
- Asignación de responsables y tiempos a cada proceso
- Traslado a inventario final
- Descuento de inventario en ventas
- Auto-gestionable (agregar referencias sin ayuda técnica)
- Escalable desde ~50 referencias

## Solución Propuesta

### Stack Tecnológico
- **Backend**: Python + Flask
- **Base de Datos**: SQLite (migrableposteriormente a PostgreSQL/MySQL)
- **Frontend**: HTML + Bootstrap + JavaScript (interfaz sencilla)
- **ORM**: SQLAlchemy

### Arquitectura del Sistema

```
ERP-Textil/
├── app/
│   ├── __init__.py
│   ├── models.py          # Modelos de base de datos
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── ordenes.py     # Rutas para órdenes
│   │   ├── referencias.py # Rutas para referencias/productos
│   │   ├── procesos.py    # Rutas para procesos
│   │   └── inventario.py  # Rutas para inventario
│   ├── templates/         # Plantillas HTML
│   └── static/            # CSS, JS, imágenes
├── config.py              # Configuración
├── requirements.txt       # Dependencias
├── run.py                 # Punto de entrada
└── database.db            # Base de datos SQLite
```

### Modelo de Datos

#### Tablas Principales:

**1. Referencias (Productos)**
- id
- codigo
- nombre
- descripcion
- ficha_tecnica (JSON con detalles)
- activo

**2. Ordenes**
- id
- numero_orden (consecutivo)
- orden_compra
- referencia_id
- cantidad
- fecha_creacion
- estado (En Proceso / Terminada / Cancelada)

**3. Procesos**
- id
- nombre (Corte, Confección, etc.)
- descripcion

**4. OrdenProceso** (relación orden-proceso)
- id
- orden_id
- proceso_id
- responsable
- tiempo_estimado (minutos)
- tiempo_real (minutos)
- estado (Pendiente / En Proceso / Completado)
- fecha_inicio
- fecha_fin

**5. Inventario**
- id
- referencia_id
- cantidad_disponible
- ultima_actualizacion

**6. MovimientosInventario** (auditoría)
- id
- referencia_id
- tipo (Entrada / Salida)
- cantidad
- orden_id (si viene de producción)
- fecha
- observaciones

## Funcionalidades Principales

### Módulo 1: Gestión de Referencias
- CRUD de referencias/productos
- Interfaz simple para agregar nuevas referencias
- Campo para ficha técnica

### Módulo 2: Gestión de Órdenes
- Crear orden de producción
- Asignar procesos a la orden
- Definir tiempos estimados
- Asignar responsables
- Seguimiento de estado

### Módulo 3: Gestión de Procesos
- Configurar procesos disponibles (Corte, Confección, etc.)
- Asignar/actualizar responsable
- Registrar tiempos reales
- Cambiar estado del proceso

### Módulo 4: Inventario
- Ver inventario actual
- Traslado automático al completar orden
- Descuento manual o automático en ventas
- Historial de movimientos

### Módulo 5: Dashboard
- Vista general de órdenes activas
- Procesos pendientes
- Alertas de tiempos excedidos
- Inventario bajo

## Fases de Implementación

### Fase 1: Base (MVP)
1. Configuración del proyecto
2. Modelos de base de datos
3. CRUD de referencias
4. CRUD de órdenes básico

### Fase 2: Procesos
5. Gestión de procesos
6. Asignación de procesos a órdenes
7. Seguimiento de tiempos

### Fase 3: Inventario
8. Traslado a inventario
9. Descuento de inventario
10. Reportes básicos

### Fase 4: Mejoras
11. Dashboard
12. Validaciones
13. Exportar datos
14. Documentación de usuario

## Decisiones Técnicas

- **SQLite**: Fácil de configurar, no requiere servidor separado, suficiente para empezar
- **Flask**: Ligero, fácil de entender y modificar
- **Bootstrap**: Interfaz responsive sin necesidad de diseño complejo
- **Sin autenticación inicial**: Se puede agregar después si es necesario

## Próximos Pasos

1. Crear estructura del proyecto
2. Implementar modelos de base de datos
3. Crear rutas y vistas básicas
4. Implementar funcionalidad core
5. Probar y documentar
