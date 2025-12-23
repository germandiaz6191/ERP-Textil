# Desplegar Odoo en AWS Lightsail (GRATIS 12 Meses)

## 🎁 Free Tier de AWS Lightsail

AWS ofrece **750 horas gratis al mes** durante los primeros **12 meses**:
- 1 instancia 24/7 durante 1 año = **$0**
- 512 MB RAM (suficiente para empezar)
- Después del año: $3.50/mes o escalar según necesidad

**¡Perfecto para tu caso!**

---

## 🚀 Paso 1: Crear Cuenta AWS

### 1.1 Registrarse

1. Ir a: https://aws.amazon.com
2. Click "Crear una cuenta de AWS"
3. Completar datos:
   - Email
   - Contraseña
   - Nombre de cuenta AWS
4. **Información de contacto**:
   - Tipo: Personal
   - Nombre completo
   - Teléfono
   - Dirección
5. **Información de pago**:
   - Tarjeta de crédito (verificación de $1 USD temporal)
   - **No te cobran si usas Free Tier**
6. **Verificación de identidad**:
   - Código por SMS o llamada
7. **Seleccionar plan**: Free (Básico)
8. **Confirmar email**

### 1.2 Acceder a la Consola

1. Ir a: https://console.aws.amazon.com
2. Login con tu cuenta
3. En barra de búsqueda superior: escribir "Lightsail"
4. Click en "Lightsail"

---

## 🖥️ Paso 2: Crear Instancia Lightsail

### 2.1 Configuración Inicial

1. En Lightsail Dashboard, click **"Create instance"**

2. **Instance location** (Ubicación):
   - Región: `US East (N. Virginia)` o `US East (Ohio)` (más cercano a Colombia)
   - Zona: Dejar por defecto (us-east-1a)

3. **Pick your instance image**:
   - Platform: **Linux/Unix**
   - Blueprint: **OS Only** → **Ubuntu 22.04 LTS**

4. **Instance plan**:
   - Seleccionar: **$3.50 USD/month** (512 MB RAM, 1 vCPU, 20 GB SSD)
   - Este plan está cubierto por Free Tier (gratis 12 meses)
   - Verás etiqueta "First 3 months free"

5. **Name your instance**:
   - Nombre: `odoo-textil`

6. **Click "Create instance"**

7. **Esperar 2-3 minutos** hasta que el estado sea "Running" (verde)

### 2.2 Configurar Firewall (Networking)

1. Click en tu instancia `odoo-textil`
2. Ir a pestaña **"Networking"**
3. En "IPv4 Firewall", click **"Add rule"**:
   - Application: **Custom**
   - Protocol: **TCP**
   - Port: **8069**
   - Click "Create"

Ahora deberías tener:
- SSH (22) - ya viene
- HTTP (80) - ya viene
- Custom TCP (8069) - recién agregado ✅

---

## 🔧 Paso 3: Conectar a la Instancia

### 3.1 Desde el Navegador (Fácil)

1. En tu instancia, click en el ícono de terminal (naranja)
2. Se abre terminal en el navegador
3. ¡Listo! Ya estás conectado como `ubuntu`

### 3.2 Desde SSH (Alternativo)

Si prefieres usar tu terminal local:

1. En Lightsail, ir a **"Account" → "SSH keys"**
2. Descargar la llave (.pem)
3. En tu terminal local:

```bash
chmod 400 ~/Downloads/LightsailDefaultKey-us-east-1.pem
ssh -i ~/Downloads/LightsailDefaultKey-us-east-1.pem ubuntu@TU_IP_PUBLICA
```

(Reemplaza TU_IP_PUBLICA con la IP que ves en el dashboard)

---

## 📦 Paso 4: Instalar Odoo (Instalación Nativa)

Una vez conectado a la terminal de tu instancia:

### 4.1 Actualizar Sistema

```bash
sudo apt update
sudo apt upgrade -y
```

### 4.2 Instalar PostgreSQL

```bash
# Instalar PostgreSQL
sudo apt install postgresql -y

# Crear usuario de base de datos para Odoo
sudo su - postgres -c "createuser -s odoo"
sudo su - postgres -c "psql -c \"ALTER USER odoo WITH PASSWORD 'odoo_password_123';\""
```

### 4.3 Instalar Dependencias de Odoo

```bash
# Instalar dependencias del sistema
sudo apt install -y python3-pip python3-dev libxml2-dev libxslt1-dev \
  libldap2-dev libsasl2-dev libtiff5-dev libjpeg8-dev libopenjp2-7-dev \
  zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev libharfbuzz-dev \
  libfribidi-dev libxcb1-dev libpq-dev git node-less npm wkhtmltopdf

# Instalar wkhtmltopdf (para reportes PDF)
sudo apt install -y wkhtmltopdf
```

### 4.4 Crear Usuario Odoo

```bash
# Crear usuario del sistema para Odoo
sudo useradd -m -U -r -d /opt/odoo -s /bin/bash odoo
```

### 4.5 Descargar Odoo

```bash
# Descargar Odoo 17.0
sudo su - odoo -c "git clone https://github.com/odoo/odoo --depth 1 --branch 17.0 /opt/odoo/odoo"
```

### 4.6 Crear Entorno Virtual e Instalar Dependencias Python

```bash
# Instalar dependencias Python
sudo su - odoo -c "cd /opt/odoo/odoo && pip3 install -r requirements.txt"
```

**Nota**: Esta instalación toma 5-10 minutos. Espera a que termine.

### 4.7 Crear Archivo de Configuración

```bash
sudo nano /etc/odoo.conf
```

Pega este contenido:

```ini
[options]
admin_passwd = admin_CAMBIAR_ESTO_123
db_host = localhost
db_port = 5432
db_user = odoo
db_password = odoo_password_123
addons_path = /opt/odoo/odoo/addons
data_dir = /opt/odoo/.local/share/Odoo
logfile = /var/log/odoo/odoo.log
log_level = info
```

Guardar: `Ctrl+O`, `Enter`, `Ctrl+X`

### 4.8 Crear Directorio de Logs

```bash
sudo mkdir -p /var/log/odoo
sudo chown odoo:odoo /var/log/odoo
```

### 4.9 Crear Servicio Systemd

```bash
sudo nano /etc/systemd/system/odoo.service
```

Pega este contenido:

```ini
[Unit]
Description=Odoo ERP
Documentation=https://www.odoo.com
After=network.target postgresql.service

[Service]
Type=simple
User=odoo
ExecStart=/opt/odoo/odoo/odoo-bin -c /etc/odoo.conf
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Guardar: `Ctrl+O`, `Enter`, `Ctrl+X`

### 4.10 Iniciar Odoo

```bash
# Recargar systemd
sudo systemctl daemon-reload

# Iniciar Odoo
sudo systemctl start odoo

# Habilitar inicio automático
sudo systemctl enable odoo

# Verificar que está corriendo
sudo systemctl status odoo
```

Deberías ver: **"active (running)"** en verde ✅

Si hay error, ver logs:
```bash
sudo journalctl -u odoo -f
```

---

## 🌐 Paso 5: Acceder a Odoo

1. **Obtener tu IP pública**:
   - En Lightsail dashboard, ver la IP de tu instancia
   - Ejemplo: `54.123.45.67`

2. **Abrir navegador**:
   - Ir a: `http://TU_IP:8069`
   - Ejemplo: `http://54.123.45.67:8069`

3. **Crear Base de Datos**:
   - Master Password: `admin_CAMBIAR_ESTO_123`
   - Database Name: `textil_erp`
   - Email: tu email
   - Password: tu contraseña
   - Language: Spanish / Español
   - Country: Colombia
   - Demo data: ❌ (desmarcar)
   - Click **"Create database"**

4. **Esperar 2-3 minutos** mientras se crea la base de datos

5. **¡Listo!** Ya estás en Odoo 🎉

---

## 📱 Paso 6: Instalar Módulos

Una vez dentro de Odoo:

1. **Ir a Apps** (menú superior)
2. **Quitar filtro** "Apps" para ver todos los módulos
3. **Instalar en este orden**:
   - ✅ **Inventory** (Inventario)
   - ✅ **Manufacturing** (Fabricación/MRP)
   - ✅ **Sales** (Ventas)
   - ✅ **Purchase** (Compras)

4. **Esperar** a que cada módulo instale (1-2 min c/u)

---

## 📊 Paso 7: Importar Datos Iniciales

### 7.1 Descargar Archivos CSV

Desde tu computadora local, descarga los archivos del repositorio:
- `odoo-setup/data/centros_trabajo.csv`
- `odoo-setup/data/productos_ejemplo.csv`

### 7.2 Importar Centros de Trabajo

1. En Odoo: **Manufacturing → Configuration → Work Centers**
2. Click en ⚙️ → **Import records**
3. Upload `centros_trabajo.csv`
4. Verificar mapeo de columnas
5. **Import**

### 7.3 Importar Productos

1. **Inventory → Products → Products**
2. Click en ⚙️ → **Import records**
3. Upload `productos_ejemplo.csv`
4. Verificar mapeo
5. **Import**

---

## 🔒 Paso 8: Seguridad (IMPORTANTE)

### 8.1 Cambiar Password Admin de Odoo

```bash
sudo nano /etc/odoo.conf
```

Cambiar:
```ini
admin_passwd = TU_PASSWORD_SUPER_SEGURO_AQUI
```

Reiniciar Odoo:
```bash
sudo systemctl restart odoo
```

### 8.2 Configurar Firewall UFW

```bash
# Habilitar firewall
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 8069/tcp  # Odoo
sudo ufw enable

# Verificar
sudo ufw status
```

### 8.3 Crear Usuario SSH (No usar Ubuntu)

```bash
# Crear tu usuario
sudo adduser tuusuario

# Agregar a sudoers
sudo usermod -aG sudo tuusuario

# Probar login
# (En otra terminal) ssh -i llave.pem tuusuario@TU_IP
```

---

## 🌍 Paso 9: (Opcional) Dominio + HTTPS

Si tienes un dominio (ej: `miempresa.com`):

### 9.1 Configurar IP Estática en Lightsail

1. En Lightsail, tu instancia
2. Pestaña **"Networking"**
3. Sección **"Public IP"**
4. Click **"Create static IP"**
5. Nombre: `odoo-textil-ip`
6. **Create**

Ahora tu IP no cambiará nunca.

### 9.2 Configurar DNS

En tu proveedor de dominio (GoDaddy, Namecheap, etc.):

1. Crear registro DNS:
   - Type: **A**
   - Name: **odoo** (o @)
   - Value: **TU_IP_ESTATICA**
   - TTL: 3600

Ejemplo: `odoo.miempresa.com` → `54.123.45.67`

### 9.3 Instalar Nginx y SSL

```bash
# Instalar Nginx
sudo apt install nginx certbot python3-certbot-nginx -y

# Configurar Nginx
sudo nano /etc/nginx/sites-available/odoo
```

Pegar:

```nginx
server {
    listen 80;
    server_name odoo.miempresa.com;

    location / {
        proxy_pass http://localhost:8069;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Activar:

```bash
sudo ln -s /etc/nginx/sites-available/odoo /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

Obtener SSL gratis:

```bash
sudo certbot --nginx -d odoo.miempresa.com
```

Ahora accedes: `https://odoo.miempresa.com` 🔒

---

## 💾 Paso 10: Backups Automáticos

### 10.1 Crear Script de Backup

```bash
sudo nano /usr/local/bin/backup-odoo.sh
```

Pegar:

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/ubuntu/backups"

mkdir -p $BACKUP_DIR

# Backup de base de datos
sudo -u postgres pg_dump textil_erp > $BACKUP_DIR/odoo_$DATE.sql

# Backup de filestore
sudo tar -czf $BACKUP_DIR/filestore_$DATE.tar.gz /opt/odoo/.local/share/Odoo/filestore

# Borrar backups antiguos (más de 7 días)
find $BACKUP_DIR -name "odoo_*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "filestore_*.tar.gz" -mtime +7 -delete

echo "Backup completado: $DATE"
```

Dar permisos:

```bash
sudo chmod +x /usr/local/bin/backup-odoo.sh
```

### 10.2 Programar Backup Diario

```bash
sudo crontab -e
```

Agregar al final:

```
0 2 * * * /usr/local/bin/backup-odoo.sh >> /var/log/odoo-backup.log 2>&1
```

Backup automático todos los días a las 2am ✅

---

## 💰 Costos y Free Tier

### Free Tier (Primeros 12 Meses)

| Servicio | Free Tier | Después |
|----------|-----------|---------|
| Lightsail $3.50/mes | ✅ Gratis (750 hrs/mes) | $3.50/mes |
| IP Estática | ✅ Gratis (1 IP) | Gratis si está adjunta |
| Transferencia | ✅ 1 TB gratis | $0.09/GB extra |
| Snapshots (backups) | Primero gratis | $0.05/GB/mes |

**Total primer año**: $0
**Total después**: ~$3.50-5/mes

### Escalabilidad

Si necesitas más recursos después:

| Plan | RAM | CPU | SSD | Costo/mes |
|------|-----|-----|-----|-----------|
| Actual | 512 MB | 1 | 20 GB | $3.50 |
| Upgrade | 1 GB | 1 | 40 GB | $5 |
| Upgrade | 2 GB | 1 | 60 GB | $10 |
| Upgrade | 4 GB | 2 | 80 GB | $20 |

**Un click y escalas** sin perder datos.

---

## 🔧 Comandos Útiles

### Ver Estado de Odoo

```bash
sudo systemctl status odoo
```

### Reiniciar Odoo

```bash
sudo systemctl restart odoo
```

### Ver Logs en Tiempo Real

```bash
sudo tail -f /var/log/odoo/odoo.log
```

### Detener Odoo

```bash
sudo systemctl stop odoo
```

### Iniciar Odoo

```bash
sudo systemctl start odoo
```

### Actualizar Odoo

```bash
sudo su - odoo
cd /opt/odoo/odoo
git pull origin 17.0
exit
sudo systemctl restart odoo
```

---

## 📱 Acceso Móvil

1. **Play Store / App Store**: Buscar "Odoo"
2. **Instalar** app oficial
3. **Configurar**:
   - URL: `http://TU_IP:8069` o `https://odoo.miempresa.com`
   - Database: `textil_erp`
   - Username: tu usuario
   - Password: tu password

---

## 🎯 Checklist Completo

- [ ] Crear cuenta AWS
- [ ] Crear instancia Lightsail (gratis)
- [ ] Configurar firewall (puerto 8069)
- [ ] Conectar por SSH/terminal
- [ ] Instalar PostgreSQL
- [ ] Instalar Odoo
- [ ] Crear servicio systemd
- [ ] Iniciar Odoo
- [ ] Acceder http://TU_IP:8069
- [ ] Crear base de datos textil_erp
- [ ] Instalar módulos (MRP, Inventory, Sales)
- [ ] Importar centros de trabajo
- [ ] Importar productos ejemplo
- [ ] Cambiar password admin
- [ ] Configurar backups automáticos
- [ ] (Opcional) Configurar dominio + HTTPS
- [ ] Probar app móvil

---

## 🚨 Solución de Problemas

### Odoo no inicia

```bash
# Ver logs
sudo journalctl -u odoo -n 50

# Verificar PostgreSQL
sudo systemctl status postgresql

# Verificar permisos
sudo chown -R odoo:odoo /opt/odoo
```

### No puedo acceder desde navegador

```bash
# Verificar que Odoo está corriendo
sudo systemctl status odoo

# Verificar firewall de Lightsail
# Ir a Networking → IPv4 Firewall → Debe tener puerto 8069

# Verificar firewall UFW
sudo ufw status
```

### Error de memoria (512 MB limitado)

Si la instancia es muy lenta:

1. En Lightsail, ir a tu instancia
2. Click en los 3 puntos → **Change instance plan**
3. Seleccionar $5/mes (1GB RAM)
4. Confirmar

### Base de datos no se crea

```bash
# Verificar logs de PostgreSQL
sudo tail -f /var/log/postgresql/postgresql-*.log

# Verificar usuario odoo en PostgreSQL
sudo -u postgres psql -c "\du"
```

---

## ⏱️ Tiempo Total de Instalación

- **Crear cuenta AWS**: 10 min
- **Crear instancia**: 3 min
- **Instalar dependencias**: 10 min
- **Instalar Odoo**: 10 min
- **Configurar y probar**: 10 min

**Total: ~45 minutos** (primera vez)

---

## 🎓 Próximos Pasos

Ahora que tienes Odoo funcionando en AWS Lightsail:

1. ✅ Seguir guía: `odoo-setup/FLUJO_TRABAJO_TEXTIL.md`
2. ✅ Crear tus centros de trabajo
3. ✅ Crear tus primeros productos
4. ✅ Configurar BoMs (Bill of Materials)
5. ✅ Crear primera orden de producción
6. ✅ Completar flujo completo
7. ✅ Escalar a tus ~50 referencias

---

## 💡 Ventajas de AWS Lightsail vs Otros

| Aspecto | AWS Lightsail | DigitalOcean | Hetzner |
|---------|---------------|---------------|---------|
| **Free Tier** | ✅ 12 meses | ❌ | ❌ |
| **Costo después** | $3.50/mes | $6/mes | €5/mes |
| **Infraestructura** | AWS | Buena | Buena |
| **Escalabilidad** | A EC2/RDS | Limitada | Limitada |
| **Snapshots** | ✅ Fácil | ✅ | ✅ |
| **Región cercana** | ✅ Virginia/Ohio | ✅ Toronto | ❌ Europa |

**Winner**: AWS Lightsail (gratis + AWS + escalable) ✅

---

¿Listo para empezar? 🚀

**Siguiente paso**: Ir a https://aws.amazon.com y crear tu cuenta.
