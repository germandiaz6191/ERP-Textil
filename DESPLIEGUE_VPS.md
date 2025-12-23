# Desplegar Odoo en VPS (Nube)

## 🌐 Opciones de VPS Recomendadas

### Opción 1: DigitalOcean (Recomendado - Simple y Económico)
- **Costo**: Desde $6/mes (1GB RAM) hasta $12/mes (2GB RAM)
- **Ventajas**: Muy fácil de usar, buena documentación
- **Droplet recomendado**: Basic - $12/mes (2GB RAM, 50GB SSD)
- **Ubicación**: Elegir región más cercana (ej: Toronto para Colombia)

### Opción 2: Hetzner (Más Económico)
- **Costo**: Desde €4.5/mes (~$5 USD)
- **Ventajas**: Muy económico, buena relación calidad-precio
- **Servidores en Europa** (puede ser más lento desde Latam)

### Opción 3: Vultr
- **Costo**: Similar a DigitalOcean ($6-12/mes)
- **Ventajas**: Tiene servidores en México (buena latencia para Colombia)

### Opción 4: AWS Lightsail
- **Costo**: Desde $5/mes
- **Ventajas**: Infraestructura de AWS, confiable
- **Desventaja**: Interfaz más compleja

### Opción 5: Contabo (Súper Económico)
- **Costo**: Desde €4/mes
- **Ventajas**: Muy barato, buenos recursos
- **Servidores en Europa/USA**

---

## 🚀 Método 1: DigitalOcean con Docker (MÁS FÁCIL)

### Paso 1: Crear Droplet en DigitalOcean

1. **Ir a**: https://www.digitalocean.com
2. **Crear cuenta** (tarjeta de crédito o PayPal)
3. **Click "Create" → "Droplets"**
4. **Configuración**:
   - **Image**: Ubuntu 22.04 LTS
   - **Plan**: Basic - $12/mes (2GB RAM, 2 vCPUs, 50GB SSD)
   - **Region**: Toronto, New York, o más cercano
   - **Authentication**: SSH key (más seguro) o Password
   - **Hostname**: odoo-textil

5. **Click "Create Droplet"**
6. **Esperar 1 minuto** → Te dan la IP del servidor

### Paso 2: Conectar al Servidor

```bash
# Desde tu terminal local
ssh root@TU_IP_AQUI

# Ejemplo:
# ssh root@159.89.123.456
```

### Paso 3: Instalar Docker en el VPS

```bash
# Actualizar sistema
apt update && apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Instalar Docker Compose
apt install docker-compose -y

# Verificar instalación
docker --version
docker-compose --version
```

### Paso 4: Crear Estructura de Odoo

```bash
# Crear directorio
mkdir -p ~/odoo-textil
cd ~/odoo-textil

# Crear archivo docker-compose.yml
cat > docker-compose.yml <<'EOF'
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: postgres
      POSTGRES_USER: odoo
      POSTGRES_PASSWORD: TU_PASSWORD_SEGURO_AQUI
    volumes:
      - odoo-db-data:/var/lib/postgresql/data
    networks:
      - odoo-network
    restart: always

  odoo:
    image: odoo:17.0
    depends_on:
      - db
    ports:
      - "8069:8069"
    environment:
      - HOST=db
      - USER=odoo
      - PASSWORD=TU_PASSWORD_SEGURO_AQUI
    volumes:
      - odoo-web-data:/var/lib/odoo
      - ./config:/etc/odoo
      - ./addons:/mnt/extra-addons
    networks:
      - odoo-network
    restart: always

volumes:
  odoo-web-data:
  odoo-db-data:

networks:
  odoo-network:
    driver: bridge
EOF

# Crear directorio de configuración
mkdir -p config addons

# Crear archivo de configuración
cat > config/odoo.conf <<'EOF'
[options]
admin_passwd = admin123_CAMBIAR_ESTO
db_host = db
db_port = 5432
db_user = odoo
db_password = TU_PASSWORD_SEGURO_AQUI
addons_path = /mnt/extra-addons
data_dir = /var/lib/odoo
EOF
```

### Paso 5: Iniciar Odoo

```bash
# Iniciar contenedores
docker-compose up -d

# Ver logs (para verificar que inició bien)
docker-compose logs -f

# Esperar 1-2 minutos hasta ver "odoo.service.server: HTTP service (werkzeug) running on"
# Presionar Ctrl+C para salir de los logs
```

### Paso 6: Configurar Firewall

```bash
# Permitir SSH, HTTP y puerto Odoo
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 8069/tcp
ufw enable

# Verificar
ufw status
```

### Paso 7: Acceder a Odoo

1. **Abrir navegador**
2. **Ir a**: `http://TU_IP:8069`
3. **Crear base de datos**:
   - Master Password: admin123_CAMBIAR_ESTO
   - Database Name: textil_erp
   - Email: tu email
   - Password: tu password
   - Language: Spanish
   - Country: Colombia

---

## 🔒 Paso Adicional: Dominio y HTTPS (Opcional pero Recomendado)

### Opción A: Con Dominio Propio (Recomendado)

Si tienes un dominio (ej: miempresa.com):

```bash
# 1. Apuntar dominio a tu IP en el DNS
# A record: odoo.miempresa.com → TU_IP

# 2. Instalar Nginx y Certbot
apt install nginx certbot python3-certbot-nginx -y

# 3. Configurar Nginx
cat > /etc/nginx/sites-available/odoo <<'EOF'
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
EOF

# 4. Activar configuración
ln -s /etc/nginx/sites-available/odoo /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx

# 5. Obtener certificado SSL gratis
certbot --nginx -d odoo.miempresa.com

# Ahora accedes por: https://odoo.miempresa.com
```

### Opción B: Sin Dominio (Solo IP)

Acceder por: `http://TU_IP:8069`

⚠️ Sin HTTPS, pero funcional para empezar.

---

## 🛠️ Método 2: Instalación Nativa en VPS

Si prefieres no usar Docker:

```bash
# 1. Conectar al VPS
ssh root@TU_IP

# 2. Actualizar sistema
apt update && apt upgrade -y

# 3. Instalar PostgreSQL
apt install postgresql -y

# 4. Crear usuario de base de datos
su - postgres -c "createuser -s odoo"
su - postgres -c "createdb odoo"

# 5. Instalar dependencias
apt install python3-pip python3-dev libxml2-dev libxslt1-dev \
  libldap2-dev libsasl2-dev libtiff5-dev libjpeg8-dev libopenjp2-7-dev \
  zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev libharfbuzz-dev \
  libfribidi-dev libxcb1-dev libpq-dev git node-less npm wkhtmltopdf -y

# 6. Crear usuario odoo
useradd -m -U -r -d /opt/odoo -s /bin/bash odoo

# 7. Descargar Odoo
su - odoo -c "git clone https://github.com/odoo/odoo --depth 1 --branch 17.0 /opt/odoo/odoo"

# 8. Instalar dependencias Python
su - odoo -c "cd /opt/odoo/odoo && pip3 install -r requirements.txt"

# 9. Crear archivo de configuración
cat > /etc/odoo.conf <<'EOF'
[options]
admin_passwd = admin123_CAMBIAR
db_host = localhost
db_port = 5432
db_user = odoo
db_password = False
addons_path = /opt/odoo/odoo/addons
data_dir = /opt/odoo/.local/share/Odoo
logfile = /var/log/odoo/odoo.log
EOF

# 10. Crear directorio de logs
mkdir -p /var/log/odoo
chown odoo:odoo /var/log/odoo

# 11. Crear servicio systemd
cat > /etc/systemd/system/odoo.service <<'EOF'
[Unit]
Description=Odoo
After=postgresql.service

[Service]
Type=simple
User=odoo
ExecStart=/opt/odoo/odoo/odoo-bin -c /etc/odoo.conf

[Install]
WantedBy=multi-user.target
EOF

# 12. Iniciar servicio
systemctl daemon-reload
systemctl start odoo
systemctl enable odoo

# 13. Verificar
systemctl status odoo

# Acceder: http://TU_IP:8069
```

---

## 💰 Comparación de Costos Mensuales

| Proveedor | Plan | RAM | Costo/mes | Región |
|-----------|------|-----|-----------|---------|
| **DigitalOcean** | Basic | 2GB | $12 | Toronto/NY |
| **Hetzner** | CX21 | 4GB | €5 (~$5.5) | Europa |
| **Vultr** | Regular | 2GB | $12 | México |
| **Contabo** | Cloud VPS S | 4GB | €5 (~$5.5) | USA/Europa |
| **AWS Lightsail** | 1GB | 1GB | $5 | Virginia |

**Recomendación**: DigitalOcean $12/mes (fácil) o Hetzner €5/mes (económico)

---

## 📊 Recursos Necesarios

### Para Empezar (1-10 usuarios)
- **RAM**: 2GB mínimo
- **CPU**: 1-2 vCPUs
- **Disco**: 25-50GB SSD
- **Ancho de banda**: 1-2TB/mes

### Crecimiento (10-50 usuarios)
- **RAM**: 4-8GB
- **CPU**: 2-4 vCPUs
- **Disco**: 100GB SSD
- **Ancho de banda**: 2-4TB/mes

**Puedes empezar pequeño y escalar después.**

---

## 🔧 Mantenimiento del VPS

### Comandos Útiles

```bash
# Ver si Odoo está corriendo
docker-compose ps

# Reiniciar Odoo
docker-compose restart

# Ver logs
docker-compose logs -f odoo

# Detener Odoo
docker-compose down

# Iniciar Odoo
docker-compose up -d

# Actualizar Odoo a nueva versión
docker-compose pull
docker-compose up -d

# Backup de base de datos
docker exec -t CONTAINER_ID pg_dump -U odoo postgres > backup.sql
```

### Backups Automáticos

```bash
# Crear script de backup
cat > /root/backup-odoo.sh <<'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker exec CONTAINER_ID pg_dump -U odoo postgres > /root/backups/odoo_$DATE.sql
find /root/backups -name "odoo_*.sql" -mtime +7 -delete
EOF

chmod +x /root/backup-odoo.sh

# Agregar a cron (backup diario a las 2am)
crontab -e
# Agregar: 0 2 * * * /root/backup-odoo.sh
```

---

## 🌍 Acceso desde Múltiples Lugares

Una vez en VPS, tu equipo puede acceder:

- **Oficina**: http://TU_IP:8069
- **Casa**: http://TU_IP:8069 (internet)
- **Planta**: http://TU_IP:8069 (WiFi local)
- **Móvil**: Descargar app Odoo en Play Store/App Store

**Todos trabajan en la misma base de datos en tiempo real.**

---

## 🚨 Seguridad Importante

### 1. Cambiar Passwords por Defecto

```bash
# Editar docker-compose.yml
nano ~/odoo-textil/docker-compose.yml
# Cambiar: TU_PASSWORD_SEGURO_AQUI por password fuerte

# Editar odoo.conf
nano ~/odoo-textil/config/odoo.conf
# Cambiar: admin123_CAMBIAR_ESTO por password fuerte

# Reiniciar
docker-compose down && docker-compose up -d
```

### 2. Crear Usuario SSH (No Usar Root)

```bash
# Crear usuario
adduser tuusuario
usermod -aG sudo tuusuario

# Probar login
ssh tuusuario@TU_IP

# Deshabilitar login root (después de verificar que tuusuario funciona)
nano /etc/ssh/sshd_config
# Cambiar: PermitRootLogin no
systemctl restart sshd
```

### 3. Firewall Básico

```bash
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw allow 8069/tcp  # Odoo
ufw enable
```

---

## 📱 Aplicación Móvil

Para acceso desde celular:

1. **Play Store / App Store**: Buscar "Odoo"
2. **Instalar** la app oficial
3. **Configurar**:
   - URL: http://TU_IP:8069
   - Database: textil_erp
   - Username: tu usuario
   - Password: tu password

**Tus operarios pueden marcar procesos desde el celular en planta.**

---

## 💡 Recomendación Final

### Para Empezar Hoy

**DigitalOcean + Docker** (Método 1):
- Más fácil de configurar
- $12/mes
- Listo en 30 minutos
- Fácil de escalar

### Para Máximo Ahorro

**Hetzner + Docker**:
- €5/mes (~$5.5)
- Misma facilidad que DigitalOcean
- Servidores en Alemania (latencia aceptable)

---

## 🎯 Paso a Paso Rápido

1. **Crear cuenta en DigitalOcean** (5 min)
2. **Crear Droplet Ubuntu 22.04** (1 min)
3. **SSH al servidor** (1 min)
4. **Copiar y pegar comandos del Método 1** (15 min)
5. **Acceder a http://TU_IP:8069** (1 min)
6. **Crear base de datos** (2 min)
7. **Instalar módulos MRP** (5 min)
8. **Importar datos de `odoo-setup/data/`** (5 min)

**Total: ~30 minutos y tienes Odoo funcionando en la nube.**

---

## ✅ Checklist

- [ ] Elegir proveedor VPS
- [ ] Crear cuenta
- [ ] Crear servidor/droplet
- [ ] Conectar por SSH
- [ ] Instalar Docker
- [ ] Copiar docker-compose.yml
- [ ] Cambiar passwords
- [ ] Iniciar Odoo
- [ ] Configurar firewall
- [ ] Acceder desde navegador
- [ ] Crear base de datos
- [ ] Instalar módulos
- [ ] Importar datos iniciales
- [ ] Configurar backup automático
- [ ] (Opcional) Configurar dominio + HTTPS

---

¿Quieres que te guíe paso a paso con DigitalOcean o prefieres otro proveedor?
