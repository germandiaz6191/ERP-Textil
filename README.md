# ERP Textil - Sistema de Gestión de Producción

## ⚠️ IMPORTANTE: Migración a Odoo Recomendada

Este repositorio contiene dos soluciones:

1. **Sistema Custom** (carpeta `app/`) - Desarrollo Flask básico
2. **Odoo MRP** (carpeta `odoo-setup/`) - **✅ RECOMENDADO**

**Para producción real, se recomienda usar Odoo**. Ver `README_ODOO.md` y `ODOO_INSTALACION.md` para detalles completos.

---

## Sistema Custom (Referencia)

Sistema ERP básico diseñado específicamente para empresas textiles, que permite gestionar órdenes de producción, procesos, referencias e inventario.

## Características Principales

- **Gestión de Referencias**: Administre sus productos con códigos, descripciones y fichas técnicas
- **Órdenes de Producción**: Cree y gestione órdenes con números consecutivos y órdenes de compra
- **Gestión de Procesos**: Configure procesos (Corte, Confección, etc.) con tiempos y responsables
- **Seguimiento en Tiempo Real**: Monitoree el progreso de cada orden y proceso
- **Inventario Automático**: Traslado automático a inventario al completar órdenes
- **Historial de Movimientos**: Auditoría completa de entradas y salidas de inventario
- **Dashboard Intuitivo**: Vista general del estado de la producción

## Requisitos

- Python 3.8+
- pip

## Instalación

1. Clone el repositorio:
```bash
git clone <url-del-repositorio>
cd ERP-Textil
```

2. Instale las dependencias:
```bash
pip install -r requirements.txt
```

3. Inicialice la base de datos:
```bash
python run.py init-db
```

4. Ejecute la aplicación:
```bash
python run.py
```

5. Abra su navegador en: `http://localhost:5000`

## Uso Básico

### 1. Configurar Procesos
Primero configure los tipos de procesos que usa su empresa (ya vienen 5 procesos estándar precargados):
- Vaya a "Procesos" en el menú
- Puede editar los existentes o agregar nuevos

### 2. Crear Referencias
Agregue sus productos/referencias:
- Vaya a "Referencias"
- Click en "Nueva Referencia"
- Complete código, nombre, descripción y ficha técnica
- La ficha técnica puede incluir detalles de procesos, tiempos, balanceos, etc.

### 3. Crear Orden de Producción
Para crear una nueva orden:
- Vaya a "Órdenes"
- Click en "Nueva Orden"
- Complete los datos: número de orden, OC, referencia y cantidad
- Después de crear, asigne los procesos necesarios
- Para cada proceso defina: responsable y tiempo estimado

### 4. Seguimiento de Procesos
Para actualizar el estado de los procesos:
- Entre a la orden desde el listado
- Click en "Actualizar" en cada proceso
- Cambie el estado (Pendiente → En Proceso → Completado)
- Registre el tiempo real y responsable

### 5. Completar Orden y Trasladar a Inventario
Cuando todos los procesos estén completados:
- Entre a la orden
- Click en "Completar Orden"
- Automáticamente se traslada al inventario

### 6. Gestión de Inventario
- Vea el inventario disponible en "Inventario"
- Ajuste manualmente entradas/salidas según sea necesario
- Revise el historial de movimientos de cada referencia

## Estructura del Proyecto

```
ERP-Textil/
├── app/                    # Aplicación principal
│   ├── models.py          # Modelos de base de datos
│   ├── routes/            # Rutas/controladores
│   └── templates/         # Plantillas HTML
├── config.py              # Configuración
├── run.py                 # Punto de entrada
├── requirements.txt       # Dependencias
└── database.db           # Base de datos SQLite (se crea automáticamente)
```

## Personalización

### Agregar Nuevas Referencias
El sistema está diseñado para ser auto-gestionable. Puede agregar todas las referencias que necesite sin ayuda técnica, directamente desde la interfaz web.

### Modificar Procesos
Puede agregar, editar o desactivar procesos según las necesidades de su empresa desde la sección "Procesos".

### Escalabilidad
El sistema usa SQLite por defecto, pero puede migrar fácilmente a PostgreSQL o MySQL modificando la variable `SQLALCHEMY_DATABASE_URI` en `config.py`.

## Soporte

Para reportar problemas o sugerir mejoras, por favor abra un issue en el repositorio.

## Licencia

Este proyecto es de uso libre para la gestión interna de empresas textiles.
