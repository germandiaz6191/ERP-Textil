# 🚀 Guía Completa: Desplegar ERP Textil en AWS Lightsail

**Guía paso a paso para principiantes** - Instalación automatizada con `install.sh`

⏱️ **Tiempo total:** 30 minutos
💰 **Costo:** GRATIS por 12 meses (AWS Free Tier)

---

## 📋 Lo que vas a hacer:

1. ✅ Crear cuenta en AWS (si no tienes)
2. ✅ Crear servidor en Lightsail
3. ✅ Conectarte por SSH (desde el navegador, fácil)
4. ✅ Clonar el repositorio
5. ✅ Ejecutar `install.sh`
6. ✅ Acceder a tu ERP

---

# PARTE 1: Crear Cuenta AWS (10 minutos)

## Paso 1.1: Ir a AWS

🔗 Abre en tu navegador: https://aws.amazon.com

Click en **"Crear una cuenta de AWS"** (arriba a la derecha)

## Paso 1.2: Completar Registro

Te pedirá:
- ✉️ **Email** (usa uno que revises)
- 🔑 **Contraseña** (guárdala bien)
- 👤 **Nombre de cuenta** (ej: "ERP-Textil-MiEmpresa")

Click **Continuar**

## Paso 1.3: Información de Contacto

- Selecciona: **"Personal"** (para uso propio)
- Completa: Nombre, teléfono, dirección

## Paso 1.4: Información de Pago

⚠️ **IMPORTANTE:**
- Pedirá tarjeta de crédito/débito
- **NO te van a cobrar** durante el Free Tier (12 meses)
- Es solo para verificación

Ingresa los datos de tu tarjeta.

## Paso 1.5: Verificación de Identidad

- Te llamarán o enviarán SMS
- Ingresa el código que recibes
- Espera validación (1-2 minutos)

## Paso 1.6: Seleccionar Plan

- Selecciona: **"Plan de soporte Basic (gratuito)"**
- Click **Completar registro**

✅ **¡Cuenta creada!** Ahora puedes acceder a la consola de AWS

---

# PARTE 2: Crear Servidor en Lightsail (5 minutos)

## Paso 2.1: Acceder a Lightsail

Una vez dentro de AWS:

1. En la barra de búsqueda arriba, escribe: **"Lightsail"**
2. Click en **"Amazon Lightsail"**

O ve directo a: https://lightsail.aws.amazon.com

## Paso 2.2: Crear Instancia

Click en el botón naranja: **"Crear instancia"**

## Paso 2.3: Seleccionar Ubicación

**Ubicación de la instancia:**
- **Región:** Selecciona la más cercana a ti
  - Colombia/Latinoamérica: `US East (Norte de Virginia)` o `São Paulo`
  - España: `Europe (Frankfurt)`

Click **Cambiar zona de disponibilidad** → Dejar la que sugiere

## Paso 2.4: Seleccionar Sistema Operativo

**Seleccionar imagen de la instancia:**

1. Click en **"Linux/Unix"**
2. Click en **"Solo sistema operativo"**
3. Selecciona: **"Ubuntu 22.04 LTS"** o **"Ubuntu 24.04 LTS"** (la que esté disponible)

💡 **El script install.sh es compatible con cualquier versión de Ubuntu**
- Detecta automáticamente la versión de Python
- Ajusta las dependencias según sea necesario
- Funciona con Ubuntu 20.04, 22.04, 24.04 sin problemas

## Paso 2.5: Seleccionar Plan

**Elige tu plan de instancia:**

⚠️ **IMPORTANTE - Recomendación de RAM:**

**Opción Recomendada** (1 GB RAM):
- Selecciona: **"$5 USD"** (1 GB RAM, 1 vCPU, 40 GB SSD)
- ✅ También es Free Tier (12 meses gratis)
- ✅ Odoo funciona perfecto sin ajustes
- ✅ Mejor rendimiento

**Opción Mínima** (512 MB RAM):
- Selecciona: **"$3.50 USD"** (512 MB RAM, 1 vCPU, 20 GB SSD)
- ⚠️ Requiere configuración adicional (ver Paso 5.1)
- ⚠️ Rendimiento limitado
- ✅ También es Free Tier

💡 **Ambas opciones son GRATIS por 12 meses** - Recomendamos 1 GB para evitar problemas de memoria.

## Paso 2.6: Nombrar Instancia

**Identifica tu instancia:**
- Escribe un nombre: `ERP-Textil-Produccion`
- (Puedes crear varias después)

## Paso 2.7: Crear

Click en **"Crear instancia"** (botón naranja abajo)

⏳ **Espera 1-2 minutos** mientras se crea...

✅ Verás: Estado **"En ejecución"** con una luz verde

---

# PARTE 3: Conectarte al Servidor (2 minutos)

## Paso 3.1: Ver tu Instancia

En Lightsail, verás tu instancia:
```
┌─────────────────────────────────┐
│ ERP-Textil-Produccion          │
│ ● En ejecución                  │
│ Ubuntu 22.04                    │
│ IP: 12.34.56.78                │ ← Tu IP pública
└─────────────────────────────────┘
```

🔴 **IMPORTANTE:** Anota tu **IP pública** (ej: `12.34.56.78`), la necesitarás después.

## Paso 3.2: Conectar por SSH (Desde el Navegador)

**Opción FÁCIL** (no necesitas programas):

1. Click en tu instancia `ERP-Textil-Produccion`
2. Click en la pestaña **"Conectar"** (arriba)
3. Click en **"Conectar usando SSH"**

Se abrirá una **terminal en el navegador** 🎉

Verás algo como:
```bash
ubuntu@ip-172-26-3-45:~$ _
```

✅ **¡Ya estás conectado al servidor!**

---

# PARTE 4: Instalar el ERP (10 minutos)

Ahora simplemente copia y pega estos comandos en la terminal:

## Paso 4.1: Actualizar el Sistema

```bash
sudo apt update
```

Espera 30 segundos... ✅

## Paso 4.2: Instalar Git

```bash
sudo apt install git -y
```

Espera 1 minuto... ✅

## Paso 4.3: Clonar el Repositorio

**Opción A - Rama con deployment (Recomendado):**

```bash
git clone -b claude/audio-client-analyzer-H7s2e https://github.com/germandiaz6191/ERP-Textil.git
```

**Opción B - Rama main (si ya mergeaste los cambios):**

```bash
git clone https://github.com/germandiaz6191/ERP-Textil.git
```

💡 **Usa Opción A** si no has mergeado los cambios a main todavía.

Verás:
```
Cloning into 'ERP-Textil'...
remote: Enumerating objects: 156, done.
remote: Counting objects: 100% (156/156), done.
...
```

✅ Listo en 10 segundos

## Paso 4.4: Entrar al Directorio

```bash
cd ERP-Textil/deployment
```

## Paso 4.5: Configurar Variables

⚠️ **IMPORTANTE**: NO necesitas tener base de datos creada. Vas a **INVENTAR** las passwords que el sistema usará.

**Copiar plantilla:**
```bash
cp config.env.example config.env
```

**Editar configuración:**
```bash
nano config.env
```

Se abrirá un editor. Verás:
```bash
# Base de datos
DB_PASSWORD="CambiaEstaPassword123!"
ADMIN_PASSWORD="MasterPassword2024!"
```

**🔑 Cambiar passwords (inventa passwords nuevas):**

1. Usa las flechas del teclado para moverte
2. Borra las contraseñas de ejemplo
3. **Escribe passwords que TÚ inventes** (serán las que usarás después)
4. **ANÓTALAS en un papel o celular** - las necesitarás

Ejemplo de cómo debería quedar:
```bash
DB_PASSWORD="MiPasswordTextil2024!"
ADMIN_PASSWORD="MasterSegura456!"
```

💡 **Qué hace el script con estas passwords:**
- Crea la base de datos PostgreSQL con `DB_PASSWORD`
- Configura Odoo con `ADMIN_PASSWORD`
- Después las usarás en el navegador para acceder

**Guardar y salir:**
1. Presiona `Ctrl + X`
2. Te pregunta "Save modified buffer?" → Escribe `Y` (sí)
3. Te pregunta el nombre → Presiona `Enter`

✅ Guardado - El script usará estas passwords para configurar TODO automáticamente

## Paso 4.6: Ejecutar Instalación Automática

**¡El momento de la verdad!** 🚀

```bash
sudo ./install.sh
```

Te preguntará:
```
¿Continuar con la instalación? (s/n):
```

Escribe `s` y presiona Enter.

⏳ **Ahora espera 10-15 minutos** mientras instala TODO automáticamente:

Verás algo como:
```
================================================
  INSTALACIÓN ODOO 17 - ERP TEXTIL
================================================

✓ Configuración cargada desde config.env

[1/8] Actualizando sistema...
[2/8] Instalando PostgreSQL...
[3/8] Instalando dependencias de Odoo...
[4/8] Creando usuario del sistema: odoo
[5/8] Descargando Odoo 17.0...
[6/8] Configurando directorios...
[7/8] Creando archivo de configuración...
[8/8] Configurando servicio systemd...

✓ Odoo reiniciado correctamente

================================================
  ✓ INSTALACIÓN COMPLETADA
================================================

Información de acceso:
  URL: http://12.34.56.78:8069
  Usuario DB: odoo
  Master Password: OtraPasswordSegura456!

✓ Credenciales guardadas en: CREDENCIALES.txt
```

✅ **¡LISTO!** Tu ERP está funcionando

---

## Paso 4.7: Optimizar para 512MB RAM (Solo si elegiste $3.50)

⚠️ **Si elegiste la instancia de 512MB**, necesitas hacer estos ajustes:

### Crear Swap (Memoria Virtual):

```bash
# Crear swap de 2GB
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Hacer permanente
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### Reducir Workers de Odoo:

```bash
# Editar configuración
sudo nano /etc/odoo.conf
```

Busca la línea:
```ini
workers = 2
```

Cámbiala por:
```ini
workers = 0
```

Guarda: `Ctrl+X`, `Y`, `Enter`

### Reiniciar Odoo:

```bash
sudo systemctl restart odoo
sudo systemctl status odoo
```

Debe decir `active (running)`.

💡 **Si elegiste 1GB RAM, omite este paso** - Odoo funcionará perfecto sin ajustes.

---

# PARTE 5: Acceder a tu ERP (1 minuto)

## Paso 5.1: Abrir Firewall

**IMPORTANTE:** Por defecto, Lightsail bloquea el puerto 8069.

**En la consola de Lightsail (navegador):**

1. Vuelve a la página de Lightsail
2. Click en tu instancia `ERP-Textil-Produccion`
3. Click en la pestaña **"Redes"**
4. Baja hasta **"Firewall de IPv4"**
5. Click en **"Agregar regla"**

Configura:
- **Aplicación:** Custom
- **Protocolo:** TCP
- **Puerto o rango:** `8069`
- **Origen:** Permitir todo el tráfico (0.0.0.0/0)

Click **Crear**

✅ Puerto abierto

## Paso 5.2: Acceder desde tu Navegador

Abre una nueva pestaña y ve a:
```
http://TU_IP_PUBLICA:8069
```

Por ejemplo:
```
http://12.34.56.78:8069
```

🎉 **¡Deberías ver la pantalla de Odoo!**

---

# PARTE 6: Configurar Odoo (Primera Vez)

## Pantalla Inicial

Verás un formulario:

**1. Master Password:**
- Usa la que configuraste: `OtraPasswordSegura456!`

**2. Database Name:**
- Escribe: `textil_erp`

**3. Email:**
- Tu email (será el usuario admin)

**4. Password:**
- Contraseña para entrar a Odoo (diferente a Master Password)

**5. Phone Number:**
- Opcional

**6. Language:**
- Selecciona: `Español (CO)` o tu país

**7. Country:**
- Tu país

**8. Demo data:**
- ❌ **Desmarca** esta opción (no queremos datos demo)

Click **"Crear base de datos"**

⏳ Espera 2-3 minutos...

---

# ✅ ¡LISTO! Tu ERP está funcionando

Ahora verás el dashboard de Odoo.

## Próximos Pasos:

### 1. Instalar Módulos Necesarios

Click en **"Aplicaciones"** (menú superior)

Busca e instala:
- ✅ **Manufacturing** (Fabricación)
- ✅ **Inventory** (Inventario)
- ✅ **Sales** (Ventas)

### 2. Configurar Centros de Trabajo

Ir a `FLUJO_TRABAJO_TEXTIL.md` para la guía completa.

### 3. Crear Productos

Ver `odoo-setup/data/productos_ejemplo.csv`

---

# 🔄 Comandos Útiles

## Volver a Conectarte al Servidor

1. Ir a Lightsail
2. Click en tu instancia
3. Click "Conectar usando SSH"

## Ver Estado de Odoo

```bash
sudo systemctl status odoo
```

## Ver Logs en Tiempo Real

```bash
sudo tail -f /var/log/odoo/odoo.log
```

## Reiniciar Odoo

```bash
sudo systemctl restart odoo
```

## Ver tus Credenciales

```bash
cd ~/ERP-Textil/deployment
cat CREDENCIALES.txt
```

---

# 🔄 Actualizar el Sistema (Cuando hagas cambios)

Desde tu computadora local:
```bash
git add .
git commit -m "Actualizar configuración"
git push
```

En el servidor (SSH):
```bash
cd ~/ERP-Textil/deployment
./deploy.sh
```

✅ Actualización automática

---

# 🔐 Importante: Seguridad

## Después de la Instalación:

### 1. Cambiar Puerto SSH (Opcional pero recomendado)

```bash
sudo nano /etc/ssh/sshd_config
```

Busca:
```
#Port 22
```

Cámbialo por:
```
Port 2222
```

Guarda y reinicia:
```bash
sudo systemctl restart ssh
```

**No olvides agregar el puerto 2222 en el Firewall de Lightsail**

### 2. Configurar Backups Automáticos

Ver: `deployment/README.md` sección "Backups Automáticos"

### 3. Configurar Dominio (Opcional)

Si tienes un dominio (ej: `erp.tuempresa.com`):

1. En tu proveedor de dominio, crea un registro A:
   - Host: `erp` (o `@` para usar el dominio raíz)
   - Tipo: `A`
   - Valor: Tu IP de Lightsail (ej: `12.34.56.78`)
   - TTL: 3600

2. Espera 10-30 minutos a que se propague

3. Instala Nginx y SSL:
   Ver: `deployment/README.md` sección "Configurar Dominio y HTTPS"

---

# 🐛 Problemas Comunes

## No puedo acceder a `http://IP:8069`

✅ **Verifica:**
1. Firewall de Lightsail tiene el puerto 8069 abierto
2. Odoo está corriendo: `sudo systemctl status odoo`
3. Estás usando HTTP (no HTTPS)

## "Permission denied" al ejecutar install.sh

```bash
chmod +x install.sh
sudo ./install.sh
```

## Olvidé mi Master Password

Está guardada en:
```bash
cat ~/ERP-Textil/deployment/CREDENCIALES.txt
```

## El servidor está lento

Si tienes 512MB RAM:
```bash
# Ver uso de memoria
free -h

# Reducir workers de Odoo
sudo nano /etc/odoo.conf
# Cambiar: workers = 0
sudo systemctl restart odoo
```

O actualiza a plan de 1GB ($5/mes)

## Odoo se reinicia constantemente (Error OOM)

Si ves en los logs:
```
odoo.service: Failed with result 'oom-kill'
```

**Problema:** Sin memoria RAM suficiente.

**Solución:**

```bash
# 1. Crear swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# 2. Reducir workers
sudo nano /etc/odoo.conf
# Cambiar: workers = 0

# 3. Reiniciar
sudo systemctl restart odoo
```

O mejor: **actualiza a 1GB RAM** en Lightsail (Gestionar → Cambiar plan)

---

# 💰 Costos AWS Lightsail

## Free Tier (12 meses):
- ✅ 750 horas/mes gratis (servidor 24/7)
- ✅ 512 MB RAM: $0/mes
- ✅ 1 GB RAM: $0/mes (primer mes)

## Después del Free Tier:
- 512 MB RAM: $3.50/mes
- 1 GB RAM: $5/mes
- 2 GB RAM: $10/mes

## Transferencia de Datos:
- Incluido: 1 TB/mes
- Exceso: $0.09/GB

Para un ERP textil pequeño/mediano, **nunca llegarás a 1 TB/mes**.

---

# 📱 Acceso desde Celular

Odoo tiene **app móvil oficial**:

📥 **Descargar:**
- Android: [Google Play](https://play.google.com/store/apps/details?id=com.odoo.mobile)
- iOS: [App Store](https://apps.apple.com/app/odoo/id1272543640)

**Configurar:**
1. URL: `http://TU_IP:8069`
2. Database: `textil_erp`
3. Email: tu email
4. Password: tu contraseña

---

# 📞 Soporte

## Documentación:
- `deployment/README.md` - Deployment completo
- `FLUJO_TRABAJO_TEXTIL.md` - Flujo de trabajo
- `ODOO_INSTALACION.md` - Instalación manual

## Recursos Odoo:
- [Documentación Oficial](https://www.odoo.com/documentation/17.0/)
- [Foro Comunidad](https://www.odoo.com/forum)
- [YouTube Tutorials](https://youtube.com/results?search_query=odoo+17+tutorial)

## Issues GitHub:
https://github.com/germandiaz6191/ERP-Textil/issues

---

# ✅ Checklist Completo

- [ ] Crear cuenta AWS
- [ ] Crear instancia Lightsail Ubuntu 22.04
- [ ] Conectar por SSH
- [ ] Clonar repositorio
- [ ] Configurar `config.env`
- [ ] Ejecutar `install.sh`
- [ ] Abrir puerto 8069 en firewall
- [ ] Acceder a `http://IP:8069`
- [ ] Crear base de datos
- [ ] Instalar módulos (Manufacturing, Inventory, Sales)
- [ ] Configurar centros de trabajo
- [ ] Crear primer producto
- [ ] Probar orden de producción
- [ ] Configurar backups (opcional)
- [ ] Configurar dominio (opcional)

---

**¡Ahora tienes tu ERP Textil funcionando en la nube!** 🎉

¿Problemas? Revisa la sección 🐛 "Problemas Comunes" o consulta `deployment/README.md`
