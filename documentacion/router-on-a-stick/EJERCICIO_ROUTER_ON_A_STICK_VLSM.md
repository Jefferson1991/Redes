# Ejercicio (tipo examen): Router-on-a-Stick + VLSM

## Enunciado

Tienes el router `R1` conectado a un switch `SW1` mediante un **enlace troncál (trunk)**. El switch debe crear VLANs para segmentar la red y el router debe enrutar entre VLANs usando **subinterfaces con encapsulación `dot1Q`**.

Debes diseñar una segmentación con **VLSM** sobre la red base `192.168.50.0/24` para las siguientes necesidades de hosts:

- VLAN 10 (Compras): **60 equipos**
- VLAN 20 (Ventas): **20 equipos**
- VLAN 30 (Inventario): **10 equipos**
- VLAN 99 (Gestión): **2 equipos** (solo infraestructura)

## Topología lógica

- El puerto del switch hacia el router es un **trunk**.
- El router usa subinterfaces:
  - `Ethernet0/0.10` -> VLAN 10
  - `Ethernet0/0.20` -> VLAN 20
  - `Ethernet0/0.30` -> VLAN 30
  - `Ethernet0/0.99` -> VLAN 99

## Entregables

1. **Plan VLSM**: subred, máscara y rangos (red, hosts, broadcast).
2. **Configuración en R1**: subinterfaces con IP y encapsulación `dot1Q`.
3. **Configuración en SW1**:
   - VLANs creadas y nombres.
   - puerto hacia el router en trunk (y VLANs permitidas).
   - SVI de gestión (`interface vlan 99`) con IP y `ip default-gateway`.

## Cálculo VLSM (guía)

Usa esta regla:

- Para `N` hosts: elige la máscara que dé al menos `N` IPs utilizables.
- (Dato útil) La cantidad de hosts utilizables es: `2^h - 2`.
  - Donde `h` es la cantidad de bits de host (por ejemplo, /26 => 6 bits de host => 62 hosts útiles).

### Tu tarea exacta

Completa el plan con:

- Red para 60 hosts
- Red para 20 hosts
- Red para 10 hosts
- Red para 2 hosts

Sugerencia de gateways (una práctica común):
- El gateway de cada VLAN en el router suele ser el **primer IP utilizable** de la subred.

## Completar la automatización

Abre `config.py` en esta carpeta y completa:

- `COMANDOS_R1` con las subinterfaces `Ethernet0/0.<vlan>` usando `encapsulation dot1Q <vlan>` e IP/máscara.
- `COMANDOS_SW1` con:
  - `vlan <id>`, `name ...`
  - `interface Ethernet0/0` trunk y `switchport trunk allowed vlan ...`
  - `interface vlan 99` con IP/máscara y `ip default-gateway <gateway_router>`.

Luego ejecuta:

- `python main.py`

## Validación (qué debe salir)

En el switch:
- `show vlan brief`
- `show interfaces trunk`
- `show ip interface brief`

En el router:
- `show ip interface brief`

Pruebas (pings):
- Desde Gestión -> gateway router en VLAN 99.
- Desde VLAN 10 -> gateway router VLAN 10.
- Desde VLAN 20 -> gateway router VLAN 20.
