# ERP Textil - Migración a Odoo MRP

## 🎯 Decisión: Usar Odoo en lugar de Sistema Custom

Después de analizar las necesidades expresadas en el audio del cliente, **Odoo Community Edition con MRP** es la mejor solución a largo plazo.

---

## ⚡ Inicio Rápido

### Instalación con Docker (5 minutos)

```bash
cd ERP-Textil
docker-compose up -d
# Abrir: http://localhost:8069
# Master Password: admin123
# Database: textil_erp
```

### Guías Completas

📖 **`ODOO_INSTALACION.md`** - Instalación paso a paso
📖 **`odoo-setup/FLUJO_TRABAJO_TEXTIL.md`** - Flujo completo para textil
📖 **`odoo-setup/GUIA_IMPORTACION.md`** - Importar datos precargados

---

## ✅ Por Qué Odoo

| Aspecto | Sistema Custom | Odoo MRP |
|---------|---------------|----------|
| Funcionalidades | Básicas | Completas |
| Escalabilidad | Limitada | Ilimitada |
| Integraciones | Ninguna | Ventas, Compras, Contabilidad |
| Reportes | Básicos | Avanzados con gráficos |
| Soporte | Ninguno | Comunidad global |
| Costo | $0 | $0 (Community) |
| App Móvil | No | Sí |
| Control de Calidad | No | Sí |

---

## 📋 Funcionalidades Clave

### Gestión de Referencias
- Productos con códigos únicos
- Fichas técnicas (BoM)
- Variantes (tallas, colores)

### Órdenes de Producción
- Número consecutivo automático
- Orden de compra asociada
- Seguimiento en tiempo real

### Procesos
- Centros de trabajo: Corte, Confección, Terminación, QC, Empaque
- Asignación de responsables
- Tiempos estimados vs reales

### Inventario
- Traslado automático al completar
- Descuento automático en ventas
- Historial completo

---

## 🚀 Setup Rápido

1. Instalar Odoo (ver `ODOO_INSTALACION.md`)
2. Activar módulos: Manufacturing, Inventory, Sales
3. Importar centros de trabajo (`odoo-setup/data/centros_trabajo.csv`)
4. Importar productos ejemplo (`odoo-setup/data/productos_ejemplo.csv`)
5. Crear tu primer BoM
6. Generar orden de producción de prueba

**Tiempo total**: 2-4 horas

---

## 📊 Mapeo de Necesidades

| Necesidad (del audio) | Solución Odoo |
|----------------------|---------------|
| Referencias con fichas técnicas | Products + BoM |
| Orden con número y OC | Manufacturing Order |
| Procesos (corte, confección) | Operations en BoM |
| Asignación de responsables | Responsible en Work Orders |
| Tiempos de ciclo | Duration registrado automáticamente |
| Traslado a inventario | Automático al "Produce" |
| Descuento en ventas | Automático en Delivery |
| ~50 referencias | Sin límite |

---

## 📁 Archivos Incluidos

- **`docker-compose.yml`** - Setup rápido con Docker
- **`ODOO_INSTALACION.md`** - Guía de instalación completa
- **`odoo-setup/FLUJO_TRABAJO_TEXTIL.md`** - Flujo de trabajo detallado
- **`odoo-setup/data/`** - CSVs con datos de ejemplo
- **`app/`** - Sistema custom (referencia)

---

## 🎓 Recursos

- [Documentación Odoo MRP](https://www.odoo.com/documentation/17.0/)
- [Foro Comunidad](https://www.odoo.com/forum)
- [Videos YouTube](https://youtube.com/results?search_query=odoo+manufacturing+tutorial)

---

## ⏱️ Timeline

- **Semana 1**: Instalación y setup inicial
- **Semana 2**: Configuración de 10-20 productos
- **Semana 3**: Migración completa (~50 productos)
- **Semana 4**: Operación real

---

**Ver `ODOO_INSTALACION.md` para empezar** 🚀
