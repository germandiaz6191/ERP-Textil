#!/bin/bash

#############################################
# INSTALACIÓN AUTOMATIZADA ODOO 17 - ERP TEXTIL
# Instalación nativa (sin Docker)
# Compatible con Ubuntu 20.04/22.04
#############################################

set -e  # Detener si hay errores

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}"
echo "================================================"
echo "  INSTALACIÓN ODOO 17 - ERP TEXTIL"
echo "  Instalación Nativa Automatizada"
echo "================================================"
echo -e "${NC}"

# Verificar que sea root o tenga sudo
if [[ $EUID -ne 0 ]] && ! sudo -n true 2>/dev/null; then
   echo -e "${RED}Este script necesita privilegios de sudo${NC}"
   exit 1
fi

# Cargar configuración
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/config.env" ]; then
    source "$SCRIPT_DIR/config.env"
    echo -e "${GREEN}✓ Configuración cargada desde config.env${NC}"
else
    echo -e "${YELLOW}⚠ No se encontró config.env, usando valores por defecto${NC}"
    echo -e "${YELLOW}  Copia config.env.example a config.env y personaliza${NC}"

    # Valores por defecto
    ODOO_VERSION="17.0"
    ODOO_USER="odoo"
    ODOO_HOME="/opt/odoo"
    ODOO_PORT="8069"
    DB_USER="odoo"
    DB_PASSWORD="odoo_password_$(date +%s)"
    ADMIN_PASSWORD="admin_$(date +%s)"
fi

echo ""
echo -e "${YELLOW}Configuración de instalación:${NC}"
echo "  Usuario Odoo: $ODOO_USER"
echo "  Directorio: $ODOO_HOME"
echo "  Puerto: $ODOO_PORT"
echo "  Usuario DB: $DB_USER"
echo ""

read -p "¿Continuar con la instalación? (s/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    exit 1
fi

#############################################
# 1. ACTUALIZAR SISTEMA
#############################################
echo -e "${GREEN}[1/8] Actualizando sistema...${NC}"
sudo apt-get update -qq
sudo apt-get upgrade -y -qq

#############################################
# 2. INSTALAR POSTGRESQL
#############################################
echo -e "${GREEN}[2/8] Instalando PostgreSQL...${NC}"
sudo apt-get install -y -qq postgresql postgresql-client

# Crear usuario de base de datos
echo -e "${YELLOW}  Creando usuario PostgreSQL: $DB_USER${NC}"
sudo -u postgres psql -c "DROP USER IF EXISTS $DB_USER;" 2>/dev/null || true
sudo -u postgres psql -c "CREATE USER $DB_USER WITH CREATEDB PASSWORD '$DB_PASSWORD';"

#############################################
# 3. INSTALAR DEPENDENCIAS
#############################################
echo -e "${GREEN}[3/8] Instalando dependencias de Odoo...${NC}"
sudo apt-get install -y -qq \
    python3-pip \
    python3-dev \
    python3-venv \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libsasl2-dev \
    libldap2-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    libmysqlclient-dev \
    libjpeg-dev \
    libpq-dev \
    libjpeg8-dev \
    liblcms2-dev \
    libblas-dev \
    libatlas-base-dev \
    npm \
    node-less \
    git \
    curl \
    wget

# Instalar wkhtmltopdf (para reportes PDF)
echo -e "${YELLOW}  Instalando wkhtmltopdf...${NC}"
sudo apt-get install -y -qq wkhtmltopdf

#############################################
# 4. CREAR USUARIO ODOO
#############################################
echo -e "${GREEN}[4/8] Creando usuario del sistema: $ODOO_USER${NC}"
sudo useradd -m -d $ODOO_HOME -U -r -s /bin/bash $ODOO_USER 2>/dev/null || echo "  Usuario ya existe"

#############################################
# 5. INSTALAR ODOO
#############################################
echo -e "${GREEN}[5/8] Descargando Odoo $ODOO_VERSION...${NC}"
sudo -u $ODOO_USER git clone --depth 1 --branch $ODOO_VERSION \
    https://github.com/odoo/odoo.git $ODOO_HOME/odoo 2>/dev/null || \
    echo "  Odoo ya descargado, actualizando..."

cd $ODOO_HOME/odoo
sudo -u $ODOO_USER git pull

# Instalar dependencias de Python
echo -e "${YELLOW}  Instalando dependencias Python...${NC}"

# Detectar versión de Python
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
PYTHON_MAJOR=$(python3 -c 'import sys; print(sys.version_info[0])')
PYTHON_MINOR=$(python3 -c 'import sys; print(sys.version_info[1])')

echo -e "${YELLOW}  Detectado Python $PYTHON_VERSION${NC}"

# Crear virtual environment para Odoo
echo -e "${YELLOW}  Creando virtual environment...${NC}"
sudo -u $ODOO_USER python3 -m venv $ODOO_HOME/venv

# Actualizar pip en el venv
sudo -u $ODOO_USER $ODOO_HOME/venv/bin/pip install --upgrade pip setuptools wheel

# Ajustar gevent si es Python 3.10+
if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 10 ]; then
    echo -e "${YELLOW}  Ajustando compatibilidad de gevent para Python 3.10+...${NC}"
    # Crear requirements.txt modificado compatible con Python 3.10+
    cat $ODOO_HOME/odoo/requirements.txt | sed 's/gevent==21.8.0/gevent==23.9.1/' > /tmp/requirements-odoo.txt
    echo -e "${YELLOW}  Usando gevent 23.9.1 (compatible con Python $PYTHON_VERSION)${NC}"
    sudo -u $ODOO_USER $ODOO_HOME/venv/bin/pip install -r /tmp/requirements-odoo.txt
else
    echo -e "${YELLOW}  Usando requirements estándar${NC}"
    sudo -u $ODOO_USER $ODOO_HOME/venv/bin/pip install -r requirements.txt
fi

#############################################
# 6. CREAR DIRECTORIOS Y MÓDULOS PERSONALIZADOS
#############################################
echo -e "${GREEN}[6/8] Configurando directorios...${NC}"
sudo mkdir -p $ODOO_HOME/custom-addons
sudo mkdir -p /var/log/odoo
sudo mkdir -p /var/backups/odoo
sudo chown -R $ODOO_USER:$ODOO_USER $ODOO_HOME
sudo chown -R $ODOO_USER:$ODOO_USER /var/log/odoo
sudo chown -R $ODOO_USER:$ODOO_USER /var/backups/odoo

# Copiar módulos personalizados desde el repositorio
if [ -d "$SCRIPT_DIR/addons" ]; then
    echo -e "${YELLOW}  Copiando módulos personalizados...${NC}"
    sudo cp -r $SCRIPT_DIR/addons/* $ODOO_HOME/custom-addons/ 2>/dev/null || true
    sudo chown -R $ODOO_USER:$ODOO_USER $ODOO_HOME/custom-addons
fi

#############################################
# 7. CONFIGURAR ODOO
#############################################
echo -e "${GREEN}[7/8] Creando archivo de configuración...${NC}"

# Usar configuración del repo o crear una nueva
if [ -f "$SCRIPT_DIR/config/odoo.conf" ]; then
    echo -e "${YELLOW}  Usando configuración desde el repositorio${NC}"
    sudo cp $SCRIPT_DIR/config/odoo.conf /etc/odoo.conf
    # Reemplazar variables
    sudo sed -i "s|{{ODOO_USER}}|$ODOO_USER|g" /etc/odoo.conf
    sudo sed -i "s|{{ODOO_HOME}}|$ODOO_HOME|g" /etc/odoo.conf
    sudo sed -i "s|{{ODOO_PORT}}|$ODOO_PORT|g" /etc/odoo.conf
    sudo sed -i "s|{{DB_USER}}|$DB_USER|g" /etc/odoo.conf
    sudo sed -i "s|{{DB_PASSWORD}}|$DB_PASSWORD|g" /etc/odoo.conf
    sudo sed -i "s|{{ADMIN_PASSWORD}}|$ADMIN_PASSWORD|g" /etc/odoo.conf
else
    echo -e "${YELLOW}  Generando configuración por defecto${NC}"
    sudo bash -c "cat > /etc/odoo.conf" <<EOF
[options]
admin_passwd = $ADMIN_PASSWORD
db_host = localhost
db_port = 5432
db_user = $DB_USER
db_password = $DB_PASSWORD
addons_path = $ODOO_HOME/odoo/addons,$ODOO_HOME/custom-addons
xmlrpc_port = $ODOO_PORT
logfile = /var/log/odoo/odoo.log
log_level = info
workers = 2
max_cron_threads = 1
limit_time_cpu = 600
limit_time_real = 1200
EOF
fi

sudo chown $ODOO_USER:$ODOO_USER /etc/odoo.conf
sudo chmod 640 /etc/odoo.conf

#############################################
# 8. CREAR SERVICIO SYSTEMD
#############################################
echo -e "${GREEN}[8/8] Configurando servicio systemd...${NC}"
sudo bash -c "cat > /etc/systemd/system/odoo.service" <<EOF
[Unit]
Description=Odoo ERP Textil
Documentation=https://www.odoo.com
After=network.target postgresql.service

[Service]
Type=simple
User=$ODOO_USER
Group=$ODOO_USER
ExecStart=$ODOO_HOME/venv/bin/python3 $ODOO_HOME/odoo/odoo-bin -c /etc/odoo.conf
WorkingDirectory=$ODOO_HOME/odoo
StandardOutput=journal+console
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Activar y arrancar servicio
sudo systemctl daemon-reload
sudo systemctl enable odoo
sudo systemctl start odoo

#############################################
# 9. CONFIGURAR FIREWALL (OPCIONAL)
#############################################
if command -v ufw &> /dev/null; then
    echo -e "${GREEN}Configurando firewall...${NC}"
    sudo ufw allow $ODOO_PORT/tcp
    sudo ufw allow 22/tcp
    echo "  Firewall configurado (Puerto $ODOO_PORT abierto)"
fi

#############################################
# FINALIZACIÓN
#############################################
echo ""
echo -e "${GREEN}================================================"
echo "  ✓ INSTALACIÓN COMPLETADA"
echo "================================================${NC}"
echo ""
echo "Información de acceso:"
echo "  URL: http://$(hostname -I | awk '{print $1}'):$ODOO_PORT"
echo "  Usuario DB: $DB_USER"
echo "  Master Password: $ADMIN_PASSWORD"
echo ""
echo "Comandos útiles:"
echo "  Estado del servicio: sudo systemctl status odoo"
echo "  Ver logs: sudo tail -f /var/log/odoo/odoo.log"
echo "  Reiniciar: sudo systemctl restart odoo"
echo ""
echo -e "${YELLOW}IMPORTANTE: Guarda la Master Password en un lugar seguro${NC}"
echo ""

# Guardar credenciales en archivo
CREDS_FILE="$SCRIPT_DIR/CREDENCIALES.txt"
cat > $CREDS_FILE <<EOF
===========================================
CREDENCIALES ODOO - ERP TEXTIL
Generadas: $(date)
===========================================

URL: http://$(hostname -I | awk '{print $1}'):$ODOO_PORT

PostgreSQL:
  Usuario: $DB_USER
  Contraseña: $DB_PASSWORD

Odoo Master Password: $ADMIN_PASSWORD

Ubicaciones:
  Odoo: $ODOO_HOME/odoo
  Módulos: $ODOO_HOME/custom-addons
  Config: /etc/odoo.conf
  Logs: /var/log/odoo/odoo.log

===========================================
⚠ MANTÉN ESTE ARCHIVO SEGURO
===========================================
EOF

chmod 600 $CREDS_FILE
echo -e "${GREEN}✓ Credenciales guardadas en: $CREDS_FILE${NC}"
