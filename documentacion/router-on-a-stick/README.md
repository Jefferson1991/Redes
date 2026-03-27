# Router-on-a-Stick (VLSM) - Práctica

Este mini-proyecto está pensado para estudiar una topología típica de examen:

- Un **switch** crea VLANs.
- El **router** hace el **routing inter-VLAN** usando **subinterfaces con `dot1Q`** (Router-on-a-Stick).
- La red base se segmenta con **VLSM** (distinto tamaño por requerimiento de hosts).

## Estructura

- `main.py` : ejecuta Netmiko y aplica la lista de comandos.
- `config.py`: define los parámetros de conexión y (como plantilla) las listas `COMANDOS_R1` y `COMANDOS_SW1`.
- `EJERCICIO_ROUTER_ON_A_STICK_VLSM.md`: enunciado para practicar.

## Cómo practicar

1. Abre `EJERCICIO_ROUTER_ON_A_STICK_VLSM.md`.
2. Calcula el VLSM, asigna VLANs y define gateways.
3. Completa `COMANDOS_R1` (subinterfaces) y `COMANDOS_SW1` (VLANs + trunk + SVI).
4. Ejecuta `main.py`.
