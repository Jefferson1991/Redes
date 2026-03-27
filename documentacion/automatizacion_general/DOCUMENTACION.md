# Automatización de Infraestructura de Red con Python
## Examen Práctico — DevNet Sandbox IOS XE Catalyst 8000v

---

## Tabla de Contenidos

1. [Objetivo](#1-objetivo)
2. [Requisitos Previos](#2-requisitos-previos)
3. [Instalación del Entorno](#3-instalación-del-entorno)
4. [Topología del Sandbox](#4-topología-del-sandbox)
5. [Arquitectura del Script](#5-arquitectura-del-script)
6. [Configuración Aplicada por Dispositivo](#6-configuración-aplicada-por-dispositivo)
7. [Ejecución](#7-ejecución)
8. [Problemas Encontrados y Soluciones](#8-problemas-encontrados-y-soluciones)
9. [Diagrama de Flujo](#9-diagrama-de-flujo)
10. [Estado Final Verificado](#10-estado-final-verificado)

---

## 1. Objetivo

Automatizar mediante Python la configuración de una topología de red compuesta por:
- **Switch Cisco Nexus 9K** — crear VLAN 10 y configurar puertos trunk
- **Router 1 — Catalyst 8000v** — subinterfaz con encapsulación dot1Q
- **Router 2 — Catalyst 8000v** — subinterfaz con encapsulación dot1Q

Adicionalmente se aplica hardening básico de seguridad (banner, encriptación de contraseñas, SSH v2, timeout de sesiones) y se valida la conectividad mediante ping entre routers.

---

## 2. Requisitos Previos

### Software necesario

| Herramienta | Versión mínima | Descarga |
|---|---|---|
| Python | 3.8+ | https://www.python.org/downloads/ |
| pip | Incluido con Python | — |
| VPN AnyConnect | Cualquiera | Proporcionado por DevNet al reservar el sandbox |

### Acceso al Sandbox DevNet

Reservar el sandbox **"IOS XE on Catalyst 8000v"** en DevNet. Una vez activo, conectar el VPN AnyConnect con las credenciales recibidas por correo.

---

## 3. Instalación del Entorno

### 3.1 Instalar Python

1. Descargar el instalador desde https://www.python.org/downloads/
2. Durante la instalación, marcar **"Add Python to PATH"**
3. Verificar la instalación:

```bash
python --version
pip --version
```

Salida esperada:
```
Python 3.x.x
pip xx.x from ...
```

### 3.2 Instalar las librerías necesarias

```bash
pip install netmiko paramiko
```

| Librería | Versión recomendada | Propósito |
|---|---|---|
| `netmiko` | 4.x+ | Conexión SSH a dispositivos Cisco con abstracción de CLI |
| `paramiko` | 3.x+ | Cliente SSH de bajo nivel — usado para el túnel al DevBox |

> `paramiko` generalmente se instala automáticamente como dependencia de `netmiko`, pero se declara explícitamente porque se usa directamente en el script.

### 3.3 Verificar la instalación de librerías

```bash
pip show netmiko
pip show paramiko
```

### 3.4 Conectar el VPN

Antes de ejecutar el script, conectar el VPN AnyConnect del sandbox. Sin VPN, los rangos `10.10.20.x` no son accesibles.

---

## 4. Topología del Sandbox

```
         [Tu máquina - Windows]
              |
         VPN AnyConnect (10.10.20.x accesible)
              |
    +---------+--------------------+--------------------+
    |                              |                    |
[10.10.20.40]              [10.10.20.48]        [10.10.20.50]
Switch Nexus 9K             Cat8k-1 (R1)         DevBox Ubuntu
SSH directo                 SSH directo               |
admin/RG!_Yw200          developer/C1sco12345    telnet localhost:2223
                                                      |
                                                 Cat8k-2 (R2)
                                                 cat8k-pod02
                                               developer/C1sco12345
```

### Tabla de acceso

| Dispositivo | IP | Puerto | Protocolo | Usuario | Contraseña |
|---|---|---|---|---|---|
| Switch Nexus 9K | `10.10.20.40` | 22 | SSH | `admin` | `RG!_Yw200` |
| Router 1 (Cat8k-1) | `10.10.20.48` | 22 | SSH | `developer` | `C1sco12345` |
| DevBox (Ubuntu) | `10.10.20.50` | 22 | SSH | `developer` | `C1sco12345` |
| Router 2 (Cat8k-2) | via DevBox | 2223 | Telnet consola | `developer` | `C1sco12345` |

> **Por qué Router 2 no tiene IP directa:** El DevBox ejecuta dos VMs Cat8kv mediante QEMU. Los puertos de consola serial (2222 y 2223) están enlazados a `127.0.0.1` del DevBox — solo accesibles desde el propio DevBox, no desde la red. El script resuelve esto creando un túnel SSH.

---

## 5. Arquitectura del Script

### 5.1 Estructura general

```
automatizacionRedes.py
│
├── DEVBOX (dict)               — Credenciales del DevBox para el túnel
│
├── class ConsolaRouter         — Acceso a Router 2 via DevBox
│   ├── __init__()              — SSH al DevBox + telnet + autenticación
│   ├── _esperar_prompt()       — Lectura basada en prompts (no sleeps fijos)
│   ├── send_config_set()       — Envía comandos en modo configuración
│   ├── send_command()          — Envía comandos EXEC
│   ├── save_config()           — Ejecuta write memory
│   └── disconnect()            — Cierra la sesión
│
├── devices (dict)              — Parámetros de conexión por dispositivo
│                                 'tipo': 'netmiko' o 'consola'
├── config_commands (dict)      — Comandos CLI organizados por dispositivo
│
├── conectar(device_name)       — Crea la conexión según el tipo
├── enviar_comandos(...)        — Aplica config y guarda
└── main()                      — Menú interactivo 1/2/3
```

### 5.2 Dos tipos de conexión

El script maneja dos métodos de conexión con la misma interfaz:

```
Netmiko (Switch y Router 1)          ConsolaRouter (Router 2)
─────────────────────────────        ──────────────────────────────────
ConnectHandler(**params)             paramiko.SSHClient() → DevBox
    │                                    │
    └─ SSH directo al dispositivo        └─ kill sesión previa en :2223
       (10.10.20.40 / 10.10.20.48)          telnet localhost:2223
                                            Enter para despertar consola
                                            Detectar y manejar prompts
```

Ambos exponen: `send_config_set()`, `save_config()`, `send_command()`, `disconnect()`

### 5.3 Clase `ConsolaRouter` — lógica de conexión detallada

```
SSH al DevBox
    │
    ▼
Matar proceso telnet previo en :2223
(QEMU solo acepta UNA conexión simultánea)
    │
    ▼
telnet localhost 2223
    │
    ▼
Esperar prompt (hasta 15s) — _esperar_prompt()
    │
    ├─ ¿Pide Username? → enviar usuario
    ├─ ¿Pide Password? → enviar contraseña
    ├─ ¿Prompt >?      → ejecutar enable
    └─ ¿Prompt #?      → continuar
    │
    ▼
Sesión activa en modo privilegiado (#)
```

---

## 6. Configuración Aplicada por Dispositivo

### Switch Nexus 9K

```cisco
banner motd #ADVERTENCIA: Acceso autorizado únicamente a personal de TI#
vlan 10
  name VLAN_COMPARTIDA
interface Ethernet1/1
  switchport
  switchport mode trunk
  switchport trunk allowed vlan 10
  no shutdown
interface Ethernet1/2
  switchport
  switchport mode trunk
  switchport trunk allowed vlan 10
  no shutdown
```

**Verificación:**
```
VLAN  Name              Status    Ports
----  ----------------  --------  ------
10    VLAN_COMPARTIDA   active

Interface   Role  Sts  Cost
Eth1/1      Desg  FWD  4     ← Forwarding
Eth1/2      Desg  FWD  4     ← Forwarding
```

---

### Router 1 — Cat8k-1 (10.10.20.48)

```cisco
banner motd #ADVERTENCIA: Acceso autorizado únicamente a personal de TI#
service password-encryption
no ip domain-lookup
ip ssh version 2
ip ssh authentication-retries 3
ip ssh time-out 60
line vty 0 4
  exec-timeout 5 0
  transport input ssh
interface GigabitEthernet2
  no shutdown
interface GigabitEthernet2.10
  encapsulation dot1Q 10
  ip address 192.168.10.1 255.255.255.0
  no shutdown
```

**Verificación:**
```
Interface            IP-Address     OK? Method Status   Protocol
GigabitEthernet1     10.10.20.48    YES NVRAM  up       up
GigabitEthernet2     unassigned     YES NVRAM  up       up
GigabitEthernet2.10  192.168.10.1   YES manual up       up  ✓
```

---

### Router 2 — Cat8k-2 / cat8k-pod02

> **Diferencia arquitectural:** Este dispositivo QEMU (`c8k5_vm`, imagen `c8000v-2.qcow2`) tiene una sola NIC configurada. Solo presenta `GigabitEthernet1`. Se usa `GigabitEthernet1.10` como subinterfaz.

```cisco
service password-encryption
no ip domain-lookup
interface GigabitEthernet1
  no shutdown
interface GigabitEthernet1.10
  encapsulation dot1Q 10
  ip address 192.168.10.2 255.255.255.0
  no shutdown
```

**Verificación:**
```
Interface             IP-Address     OK? Method Status   Protocol
GigabitEthernet1      10.10.20.103   YES DHCP   up       up
GigabitEthernet1.10   192.168.10.2   YES manual up       up  ✓
```

---

## 7. Ejecución

### Paso 1 — Conectar VPN AnyConnect

Conectar al sandbox con las credenciales recibidas por correo de DevNet.

### Paso 2 — Ejecutar el script

```bash
python automatizacionRedes.py
```

### Paso 3 — Seleccionar opción

```
=== Automatización de Infraestructura de Red ===
REQUISITO: VPN AnyConnect del sandbox debe estar activa.

¿Qué desea configurar?
  1. Solo Switch Nexus 9K
  2. Solo Routers (R1 y R2)
  3. Todo (Switch + Routers + Validación de ping)

Seleccione opción (1-3):
```

| Opción | Dispositivos | Validación ping |
|---|---|---|
| `1` | Switch Nexus 9K | No |
| `2` | Router 1 + Router 2 | No |
| `3` | Switch + Router 1 + Router 2 | Sí — ping R2 → R1 |

### Salida esperada (opción 3)

```
[*] Conectando a 10.10.20.40 (switch_nexus) via SSH...
[+] Conexión establecida con switch_nexus.
[*] Enviando comandos a switch_nexus...
[+] Configuración aplicada y guardada en switch_nexus.

[*] Conectando a 10.10.20.48 (router1) via SSH...
[+] Conexión establecida con router1.
[*] Enviando comandos a router1...
[+] Configuración aplicada y guardada en router1.

[*] Conectando a router2 via consola del DevBox...
    [>] SSH al DevBox (10.10.20.50)...
    [>] Liberando puerto 2223 si hay sesión activa...
    [>] Abriendo consola del router (puerto 2223)...
    [>] Sesión activa en el router.
[+] Conexión establecida con router2.
[*] Enviando comandos a router2...
[+] Configuración aplicada y guardada en router2.

[*] Esperando 5 segundos para convergencia de red...
Enviando ping desde Router 2 (192.168.10.2) hacia Router 1 (192.168.10.1)...

--- Resultado Final del Ping ---
...
--------------------------------

¡Despliegue finalizado exitosamente!
```

---

## 8. Problemas Encontrados y Soluciones

### Problema 1 — `WinError 10061` al intentar conectar a los routers

**Error:**
```
[WinError 10061] No se puede establecer una conexión ya que el equipo de
destino denegó expresamente dicha conexión
```

**Causa:** Los puertos 2222/2223 del DevBox están enlazados únicamente a `127.0.0.1`. No son accesibles desde máquinas externas, ni siquiera con VPN activa.

**Solución aplicada:**
- Router 1: cambiar a SSH directo en `10.10.20.48:22` (el dispositivo tiene SSH habilitado).
- Router 2: usar `paramiko` para crear túnel SSH al DevBox, y desde ahí abrir `telnet localhost:2223`.

---

### Problema 2 — Conexión a Router 2 se quedaba colgada en `Trying 127.0.0.1...`

**Causa:** El socket QEMU (`-chardev socket,server=on,wait=off`) solo acepta **una conexión simultánea**. La sesión PuTTY del usuario (PID 3434) mantenía el socket ocupado.

**Diagnóstico realizado desde Python:**
```bash
# Ejecutado en el DevBox via paramiko:
ss -tlnp | grep "2222\|2223"
# Resultado: LISTEN 127.0.0.1:2223 — confirmado enlazado solo a localhost

ps aux | grep telnet
# Resultado: developer 3434 ... telnet localhost 2223  ← sesión activa bloqueando
```

**Solución aplicada:** Antes de conectar, el script ejecuta en el DevBox:
```bash
PID=$(ps aux | grep 'telnet localhost 2223' | grep -v grep | awk '{print $2}') \
  && [ -n "$PID" ] && kill $PID
```

---

### Problema 3 — Comandos enviados antes de obtener el prompt del router

**Causa:** La clase original usaba `time.sleep()` fijos. Si el router tardaba más de lo esperado, los comandos llegaban antes de que el dispositivo estuviera listo.

**Solución aplicada:** Método `_esperar_prompt()` que lee el buffer en tiempo real hasta detectar uno de los prompts esperados (`#`, `>`, `Username`, `Password`, `(config`):

```python
def _esperar_prompt(self, prompts, timeout=15):
    salida = ''
    inicio = time.time()
    while time.time() - inicio < timeout:
        if self.shell.recv_ready():
            chunk = self.shell.recv(4096).decode('utf-8', errors='ignore')
            salida += chunk
            if any(p in salida for p in prompts):
                break
        else:
            time.sleep(0.2)
    return salida
```

---

### Problema 4 — `interface GigabitEthernet2` inválido en Router 2

**Error:**
```
% Invalid input detected at '^' marker.
```

**Causa:** La VM QEMU `c8k5_vm` (puerto 2223) tiene una sola NIC configurada. IOS XE solo presenta `GigabitEthernet1`.

**Diagnóstico:**
```
cat8k-pod02# show interfaces summary
Interface         ...
GigabitEthernet1  ← única interfaz disponible
Vlan1
Vlan20
Vlan22
```

**Solución:** Usar `GigabitEthernet1.10` como subinterfaz en Router 2.

---

### Problema 5 — `getpass` con credenciales únicas para todos los dispositivos

**Causa:** La versión inicial pedía usuario/contraseña únicos al inicio con `getpass()`. El switch usa `admin/RG!_Yw200` y los routers usan `developer/C1sco12345`.

**Solución:** Credenciales hardcodeadas por dispositivo en el diccionario `devices` (entorno de laboratorio controlado con credenciales conocidas).

---

## 9. Diagrama de Flujo

```
Inicio
  │
  ├─ Menú: opción 1/2/3
  │
  ├─[Opción incluye switch]──── Netmiko SSH ──────→ 10.10.20.40
  │                              send_config_set()  VLAN 10 + trunk ports
  │                              save_config()
  │
  ├─[Opción incluye R1]───────── Netmiko SSH ──────→ 10.10.20.48
  │                              send_config_set()  GigabitEthernet2.10
  │                              save_config()      192.168.10.1/24
  │
  ├─[Opción incluye R2]───────── Paramiko SSH ─────→ DevBox 10.10.20.50
  │                              kill proceso :2223
  │                              telnet localhost:2223
  │                              Enter (despertar consola)
  │                              _esperar_prompt()
  │                              send_config_set()  GigabitEthernet1.10
  │                              save_config()      192.168.10.2/24
  │
  └─[Opción 3 completa]────────── ping 192.168.10.1 source GigabitEthernet1.10
                                   Mostrar resultado
                                   Cerrar todas las conexiones
                                   Fin
```

---

## 10. Estado Final Verificado

| Dispositivo | Interfaz configurada | IP asignada | Estado |
|---|---|---|---|
| Switch Nexus 9K | VLAN 10 + Eth1/1 + Eth1/2 trunk | — | Verificado ✓ |
| Router 1 (10.10.20.48) | `GigabitEthernet2.10` | `192.168.10.1/24` | UP/UP ✓ |
| Router 2 (cat8k-pod02) | `GigabitEthernet1.10` | `192.168.10.2/24` | UP/UP ✓ |

---

## Apéndice — Comandos útiles de verificación manual

### Conectar al Router 2 manualmente desde PuTTY

1. Abrir PuTTY → SSH → `10.10.20.50` (developer/C1sco12345)
2. En el DevBox ejecutar:
```bash
telnet localhost 2223
```
3. Verificar:
```
cat8k-pod02# show ip interface brief
cat8k-pod02# show running-config
```

### Verificar el Switch

```bash
# PuTTY SSH a 10.10.20.40 (admin/RG!_Yw200)
show vlan
show interfaces trunk
show cdp neighbors
```

### Verificar Router 1

```bash
# PuTTY SSH a 10.10.20.48 (developer/C1sco12345)
show ip interface brief
show running-config interface GigabitEthernet2.10
```
