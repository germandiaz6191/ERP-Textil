#!/bin/bash

#############################################
# SCRIPT DE DEPLOYMENT - ERP TEXTIL
# Actualiza módulos y configuraciones desde Git
#############################################

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}"
echo "================================================"
echo "  DEPLOYMENT ERP TEXTIL"
echo "  Actualizando desde Git..."
echo "================================================"
echo -e "${NC}"

# Configuración
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

if [ -f "$SCRIPT_DIR/config.env" ]; then
    source "$SCRIPT_DIR/config.env"
else
    echo -e "${YELLOW}⚠ config.env no encontrado, usando valores por defecto${NC}"
    ODOO_USER="odoo"
    ODOO_HOME="/opt/odoo"
fi

#############################################
# 1. ACTUALIZAR REPOSITORIO
#############################################
echo -e "${GREEN}[1/5] Actualizando repositorio Git...${NC}"
cd "$REPO_DIR"
git pull origin $(git branch --show-current)

#############################################
# 2. ACTUALIZAR ODOO CORE (opcional)
#############################################
read -p "¿Actualizar Odoo core? (s/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo -e "${GREEN}[2/5] Actualizando Odoo core...${NC}"
    cd $ODOO_HOME/odoo
    sudo -u $ODOO_USER git pull
    sudo -u $ODOO_USER python3 -m pip install --user -r requirements.txt
else
    echo -e "${YELLOW}[2/5] Omitiendo actualización de Odoo core${NC}"
fi

#############################################
# 3. ACTUALIZAR MÓDULOS PERSONALIZADOS
#############################################
echo -e "${GREEN}[3/5] Actualizando módulos personalizados...${NC}"
if [ -d "$SCRIPT_DIR/addons" ]; then
    sudo rsync -av --delete "$SCRIPT_DIR/addons/" "$ODOO_HOME/custom-addons/"
    sudo chown -R $ODOO_USER:$ODOO_USER $ODOO_HOME/custom-addons
    echo -e "${GREEN}✓ Módulos actualizados${NC}"
else
    echo -e "${YELLOW}⚠ No hay módulos personalizados en deployment/addons${NC}"
fi

#############################################
# 4. ACTUALIZAR CONFIGURACIÓN
#############################################
echo -e "${GREEN}[4/5] Actualizando configuración...${NC}"
if [ -f "$SCRIPT_DIR/config/odoo.conf" ]; then
    # Backup de configuración actual
    sudo cp /etc/odoo.conf /etc/odoo.conf.backup.$(date +%Y%m%d_%H%M%S)

    # Copiar nueva configuración
    sudo cp $SCRIPT_DIR/config/odoo.conf /etc/odoo.conf.tmp

    # Reemplazar variables
    source $SCRIPT_DIR/config.env 2>/dev/null || true
    sudo sed -i "s|{{ODOO_USER}}|$ODOO_USER|g" /etc/odoo.conf.tmp
    sudo sed -i "s|{{ODOO_HOME}}|$ODOO_HOME|g" /etc/odoo.conf.tmp
    sudo sed -i "s|{{ODOO_PORT}}|$ODOO_PORT|g" /etc/odoo.conf.tmp
    sudo sed -i "s|{{DB_USER}}|$DB_USER|g" /etc/odoo.conf.tmp
    sudo sed -i "s|{{DB_PASSWORD}}|$DB_PASSWORD|g" /etc/odoo.conf.tmp
    sudo sed -i "s|{{ADMIN_PASSWORD}}|$ADMIN_PASSWORD|g" /etc/odoo.conf.tmp

    sudo mv /etc/odoo.conf.tmp /etc/odoo.conf
    sudo chown $ODOO_USER:$ODOO_USER /etc/odoo.conf
    sudo chmod 640 /etc/odoo.conf

    echo -e "${GREEN}✓ Configuración actualizada${NC}"
fi

#############################################
# 5. REINICIAR ODOO
#############################################
echo -e "${GREEN}[5/5] Reiniciando Odoo...${NC}"
sudo systemctl restart odoo

# Esperar a que arranque
echo -n "Esperando a que Odoo inicie"
for i in {1..10}; do
    echo -n "."
    sleep 1
done
echo ""

# Verificar estado
if sudo systemctl is-active --quiet odoo; then
    echo -e "${GREEN}✓ Odoo reiniciado correctamente${NC}"
else
    echo -e "${RED}✗ Error al reiniciar Odoo${NC}"
    echo -e "${YELLOW}Ver logs: sudo journalctl -u odoo -n 50${NC}"
    exit 1
fi

#############################################
# FINALIZACIÓN
#############################################
echo ""
echo -e "${GREEN}================================================"
echo "  ✓ DEPLOYMENT COMPLETADO"
echo "================================================${NC}"
echo ""
echo "Comandos útiles:"
echo "  Ver estado: sudo systemctl status odoo"
echo "  Ver logs: sudo tail -f /var/log/odoo/odoo.log"
echo "  Reiniciar: sudo systemctl restart odoo"
echo ""
echo -e "${YELLOW}Nota: Actualiza los módulos desde Odoo web:${NC}"
echo "  Aplicaciones > Actualizar lista de aplicaciones"
echo ""
