# Módulos Personalizados - ERP Textil

Este directorio contiene los módulos personalizados de Odoo para el ERP Textil.

## Estructura

```
addons/
├── modulo_ejemplo/          # Módulo de ejemplo
│   ├── __init__.py
│   ├── __manifest__.py
│   └── models/
│       ├── __init__.py
│       └── ejemplo.py
├── erp_textil_custom/      # Tu módulo personalizado (crear aquí)
└── README.md               # Este archivo
```

## Cómo crear un nuevo módulo

1. **Crear estructura básica:**
```bash
cd deployment/addons
mkdir mi_modulo
cd mi_modulo
```

2. **Crear `__init__.py`:**
```python
from . import models
```

3. **Crear `__manifest__.py`:**
```python
{
    'name': 'Mi Módulo',
    'version': '17.0.1.0.0',
    'category': 'Manufacturing',
    'summary': 'Descripción breve',
    'depends': ['mrp'],  # Módulos de los que depende
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/mi_vista.xml',
    ],
    'installable': True,
    'application': False,
}
```

4. **Crear modelos (opcional):**
```bash
mkdir models
touch models/__init__.py
```

## Deployment

Cuando hagas cambios a los módulos:

1. **Commit y push a Git:**
```bash
git add deployment/addons/
git commit -m "Actualizar módulo personalizado"
git push
```

2. **En el servidor, ejecutar deployment:**
```bash
cd /ruta/al/repo
git pull
./deployment/deploy.sh
```

3. **Actualizar módulos en Odoo:**
   - Ir a Aplicaciones
   - Click en "Actualizar lista de aplicaciones"
   - Buscar tu módulo
   - Instalar o actualizar

## Ejemplo de módulo personalizado

Ver el directorio `modulo_ejemplo/` para una plantilla básica.

## Buenas prácticas

- ✅ Versiona tus módulos en Git
- ✅ Usa nombres descriptivos
- ✅ Documenta tus cambios
- ✅ Prueba en desarrollo antes de producción
- ✅ Declara todas las dependencias en `depends`
- ✅ Usa categorías apropiadas

## Recursos

- [Documentación Odoo 17](https://www.odoo.com/documentation/17.0/)
- [Desarrollo de módulos](https://www.odoo.com/documentation/17.0/developer/howtos.html)
