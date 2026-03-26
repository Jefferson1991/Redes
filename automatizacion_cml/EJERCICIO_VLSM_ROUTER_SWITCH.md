# Ejercicio practico: VLSM + Router-on-a-Stick (R1 y SW1)

## Escenario

Tienes una red base `192.168.20.0/24` y debes segmentarla con VLSM para:

- Compras: 60 equipos
- Ventas: 20 equipos
- Gestion/Configuracion: 2 equipos

Se trabaja con:

- 1 Router (`R1`)
- 1 Switch (`SW1`)
- Automatizacion con Python + Netmiko (`config.py` y `main.py`)

---

## Objetivo

Configurar VLANs, trunk y subinterfaces en el router para permitir conectividad entre redes (inter-VLAN routing) y gestion del switch.

---

## Parte 1: Diseno VLSM

Asignacion sugerida:

1. **Compras (60 hosts)**  
   Red: `192.168.20.0/26`  
   Rango util: `192.168.20.1 - 192.168.20.62`  
   Broadcast: `192.168.20.63`  
   Gateway: `192.168.20.1`

2. **Ventas (20 hosts)**  
   Red: `192.168.20.64/27`  
   Rango util: `192.168.20.65 - 192.168.20.94`  
   Broadcast: `192.168.20.95`  
   Gateway: `192.168.20.65`

3. **Gestion (2 hosts)**  
   Red: `192.168.20.96/30`  
   Rango util: `192.168.20.97 - 192.168.20.98`  
   Broadcast: `192.168.20.99`  
   Gateway router: `192.168.20.97`  
   SVI switch: `192.168.20.98`

---

## Parte 2: Implementacion en dispositivos

### A) Router R1 (Router-on-a-Stick)

Configurar:

- `Ethernet0/0` sin IP (`no ip address`) y activo
- Subinterfaces:
  - `Ethernet0/0.10` -> VLAN 10 -> `192.168.20.1/26`
  - `Ethernet0/0.20` -> VLAN 20 -> `192.168.20.65/27`
  - `Ethernet0/0.99` -> VLAN 99 -> `192.168.20.97/30`

### B) Switch SW1

Configurar:

- VLAN 10 = COMPRAS
- VLAN 20 = VENTAS
- VLAN 99 = GESTION
- `Ethernet0/0` como trunk al router
  - encapsulacion dot1q (si el IOS lo requiere)
  - VLANs permitidas `10,20,99`
- `Ethernet0/1` acceso VLAN 10
- `Ethernet0/2` acceso VLAN 20
- `interface vlan 99` con IP `192.168.20.98/30`
- `ip default-gateway 192.168.20.97`

---

## Parte 3: Validacion (checklist)

## En R1

- `show ip interface brief`
- `show running-config interface Ethernet0/0`
- `show running-config interface Ethernet0/0.10`
- `show running-config interface Ethernet0/0.20`
- `show running-config interface Ethernet0/0.99`

## En SW1

- `show vlan brief`
- `show interfaces trunk`
- `show interfaces Ethernet0/0 switchport`
- `show ip interface brief`
- `show running-config interface vlan 99`

## Pruebas de ping

- SW1 -> `ping 192.168.20.97`
- Host VLAN 10 -> `ping 192.168.20.1`
- Host VLAN 20 -> `ping 192.168.20.65`
- Host VLAN 10 <-> Host VLAN 20 (si se permite inter-VLAN)

---

## Parte 4: Practica con automatizacion (Netmiko)

1. Ajusta `COMANDOS_R1` y `COMANDOS_SW1` en `config.py`.
2. Ejecuta `main.py`.
3. Revisa salida del script (que imprima comandos en orden).
4. Corre checklist de validacion.
5. Si falla trunk con mensaje de encapsulacion en auto, agrega antes:

`switchport trunk encapsulation dot1q`

---

## Retos extra (para subir nivel)

1. Agregar DHCP en R1 para VLAN 10 y 20.
2. Bloquear comunicacion de Ventas hacia Compras con ACL.
3. Agregar SW2 y repetir esquema.
4. Agregar verificacion automatica con comandos `show` desde Python.
5. Crear opcion en `main.py` para "solo validacion" sin configurar.

---

## Entregable sugerido

Capturas o salida de:

- `show vlan brief`
- `show interfaces trunk`
- `show ip interface brief` (R1 y SW1)
- Pings exitosos

Y una breve explicacion de:

- Como calculaste VLSM
- Como configuraste trunk
- Que problemas encontraste y como los resolviste
