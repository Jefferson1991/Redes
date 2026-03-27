# Router-dhcp

Practica de DHCP en router Cisco usando CML Console Server.

## Objetivo

- Crear VLAN 10 y VLAN 20 en el switch.
- Usar trunk entre switch y router.
- Configurar subinterfaces en el router (Router-on-a-Stick).
- Entregar IP por DHCP desde el router a cada VLAN.

## Archivos

- `config.py`: conexion CML + comandos de R1 y SW1.
- `main.py`: ejecuta automatizacion (elige R1 o SW1).

## Uso

1. Ajusta rutas de consola en `config.py` si cambia el nombre del lab/nodo.
2. Ejecuta:
   - `python main.py`
3. Elige:
   - `1` para configurar Router DHCP
   - `2` para configurar Switch

## Verificacion sugerida

En R1:

- `show ip interface brief`
- `show ip dhcp pool`
- `show ip dhcp binding`

En SW1:

- `show interfaces trunk`
- `show vlan brief`

En un host Linux conectado a VLAN 10 o 20:

- `dhclient -v eth0`
- `ip addr show eth0`
- `ip route`
