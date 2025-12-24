# 🚀 Deployment Automatizado - ERP Textil

Sistema de instalación y deployment automatizado para Odoo 17 (instalación nativa, sin Docker).

## ✨ Características

- ✅ **Instalación automatizada** con un solo script
- ✅ **Configuración versionada** en Git
- ✅ **Portable** - instala en cualquier servidor
- ✅ **Reproducible** - misma configuración siempre
- ✅ **Módulos personalizados** versionados
- ✅ **Deployment con un comando**
- ✅ **Compatible con AWS Lightsail, VPS, etc.**

---

## 📋 Requisitos

- Ubuntu 20.04 o 22.04
- Acceso root o sudo
- Conexión a internet
- Mínimo 512MB RAM (recomendado 1GB+)

---

## 🎯 Instalación en Servidor Nuevo

### 1. Clonar repositorio

```bash
git clone https://github.com/germandiaz6191/ERP-Textil.git
cd ERP-Textil/deployment
```

### 2. Configurar variables

```bash
cp config.env.example config.env
nano config.env
```

**Cambia al menos estas variables:**
```bash
DB_PASSWORD="TuPasswordSegura123!"
ADMIN_PASSWORD="MasterPasswordSegura456!"
```

### 3. Ejecutar instalación

```bash
chmod +x install.sh
sudo ./install.sh
```

⏱️ **Tiempo estimado:** 15-20 minutos

### 4. ¡Listo!

El script te mostrará:
- URL de acceso
- Credenciales
- Comandos útiles

Las credenciales también se guardan en `CREDENCIALES.txt`

---

## 🔄 Actualizar el Sistema (Deployment)

Cuando hagas cambios (configuración, módulos, etc.):

### En tu máquina local:

```bash
# 1. Editar archivos
nano deployment/config/odoo.conf

# 2. Commit y push
git add .
git commit -m "Actualizar configuración"
git push
```

### En el servidor:

```bash
cd /ruta/al/ERP-Textil/deployment
chmod +x deploy.sh
./deploy.sh
```

Esto automáticamente:
1. ✅ Hace pull del repositorio
2. ✅ Actualiza módulos personalizados
3. ✅ Actualiza configuración
4. ✅ Reinicia Odoo

---

## 📁 Estructura del Proyecto

```
deployment/
├── install.sh              # Script de instalación automatizada
├── deploy.sh              # Script de deployment/actualización
├── config.env.example     # Plantilla de configuración
├── config.env             # Tu configuración (no se sube a Git)
├── config/
│   └── odoo.conf         # Configuración de Odoo
├── addons/               # Módulos personalizados
│   └── README.md
├── backups/              # Backups automáticos
└── README.md             # Este archivo
```

---

## 🔧 Comandos Útiles

### Ver estado del servicio
```bash
sudo systemctl status odoo
```

### Ver logs en tiempo real
```bash
sudo tail -f /var/log/odoo/odoo.log
```

### Reiniciar Odoo
```bash
sudo systemctl restart odoo
```

### Detener Odoo
```bash
sudo systemctl stop odoo
```

### Ver logs del sistema
```bash
sudo journalctl -u odoo -n 100 -f
```

---

## 🔐 Seguridad

### Después de la instalación:

1. **Cambiar passwords en producción:**
```bash
nano config.env  # Cambiar DB_PASSWORD y ADMIN_PASSWORD
./deploy.sh      # Aplicar cambios
```

2. **Configurar firewall:**
```bash
sudo ufw enable
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 8069/tcp  # Odoo
```

3. **Deshabilitar creación de BD desde web:**
   - Editar `/etc/odoo.conf`
   - Cambiar `list_db = False`
   - Reiniciar: `sudo systemctl restart odoo`

---

## 🌐 Configurar Dominio y HTTPS

### 1. Instalar Nginx

```bash
sudo apt install nginx certbot python3-certbot-nginx -y
```

### 2. Configurar Nginx

```bash
sudo nano /etc/nginx/sites-available/odoo
```

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8069;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/odoo /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 3. Obtener certificado SSL

```bash
sudo certbot --nginx -d tu-dominio.com
```

### 4. Activar modo proxy en Odoo

Edita `/etc/odoo.conf` y agrega:
```
proxy_mode = True
```

Reinicia:
```bash
sudo systemctl restart odoo
```

---

## 📦 Agregar Módulos Personalizados

### 1. Crear módulo en tu máquina local

```bash
cd deployment/addons
mkdir mi_modulo_textil
cd mi_modulo_textil

# Crear archivos básicos
touch __init__.py __manifest__.py
mkdir models views
```

### 2. Commit y push

```bash
git add deployment/addons/
git commit -m "Agregar módulo personalizado"
git push
```

### 3. Desplegar en servidor

```bash
./deployment/deploy.sh
```

### 4. Activar en Odoo

- Ir a Aplicaciones
- Click "Actualizar lista de aplicaciones"
- Buscar tu módulo
- Instalar

---

## 🔄 Migrar a Otro Servidor

Para mover tu instalación a otro servidor:

### En el servidor viejo:

```bash
# Backup de base de datos
sudo -u postgres pg_dump odoo_textil > backup_$(date +%Y%m%d).sql

# Backup de filestore (archivos adjuntos)
sudo tar -czf filestore_backup.tar.gz /opt/odoo/.local/share/Odoo/filestore
```

### En el servidor nuevo:

```bash
# 1. Clonar repo e instalar
git clone https://github.com/germandiaz6191/ERP-Textil.git
cd ERP-Textil/deployment
cp config.env.example config.env
nano config.env  # Usar MISMAS credenciales
./install.sh

# 2. Restaurar base de datos
sudo -u postgres psql < backup_20240101.sql

# 3. Restaurar filestore
sudo tar -xzf filestore_backup.tar.gz -C /

# 4. Reiniciar
sudo systemctl restart odoo
```

---

## 📊 Backups Automáticos

### Script de backup (crear en `/usr/local/bin/backup-odoo.sh`):

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/odoo"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup BD
sudo -u postgres pg_dump odoo_textil > $BACKUP_DIR/db_$DATE.sql

# Backup filestore
sudo tar -czf $BACKUP_DIR/filestore_$DATE.tar.gz /opt/odoo/.local/share/Odoo/filestore

# Eliminar backups antiguos (más de 7 días)
find $BACKUP_DIR -type f -mtime +7 -delete
```

### Automatizar con cron (diario a las 2 AM):

```bash
sudo crontab -e
```

Agregar:
```
0 2 * * * /usr/local/bin/backup-odoo.sh
```

---

## 🐛 Troubleshooting

### Odoo no inicia

```bash
# Ver logs
sudo journalctl -u odoo -n 50 --no-pager

# Verificar PostgreSQL
sudo systemctl status postgresql

# Probar manualmente
sudo -u odoo /opt/odoo/odoo/odoo-bin -c /etc/odoo.conf
```

### Puerto ocupado

```bash
# Ver qué usa el puerto 8069
sudo lsof -i :8069

# Cambiar puerto en config.env
nano config.env  # ODOO_PORT="8070"
./deploy.sh
```

### Módulo no aparece

```bash
# Verificar permisos
sudo chown -R odoo:odoo /opt/odoo/custom-addons

# Reiniciar con actualización
sudo systemctl restart odoo
```

---

## 📚 Recursos

- [Documentación Odoo 17](https://www.odoo.com/documentation/17.0/)
- [Guía de AWS Lightsail](../DESPLIEGUE_AWS_LIGHTSAIL.md)
- [Flujo de trabajo textil](../odoo-setup/FLUJO_TRABAJO_TEXTIL.md)

---

## ❓ Preguntas Frecuentes

### ¿Puedo cambiar el puerto después de instalar?

Sí, edita `config.env`, cambia `ODOO_PORT` y ejecuta `./deploy.sh`

### ¿Cómo actualizo Odoo a una nueva versión?

Ejecuta `./deploy.sh` y responde "s" cuando pregunte si actualizar Odoo core.

### ¿Funciona en otros sistemas operativos?

Está optimizado para Ubuntu. Para otras distribuciones, adapta los comandos de instalación de paquetes.

### ¿Puedo usar Docker en su lugar?

Este deployment es nativo. Si prefieres Docker, consulta `ODOO_INSTALACION.md`.

---

## 📝 Soporte

Para issues y mejoras: https://github.com/germandiaz6191/ERP-Textil/issues

---

**Hecho con ❤️ para producción textil**
