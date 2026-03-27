from netmiko import ConnectHandler
from consola import ConsolaRouter
from config import SWITCH, ROUTER1, DEVBOX
from config import COMANDOS_SWITCH, COMANDOS_ROUTER1, COMANDOS_ROUTER2
import time

def configurar(conexion, comandos, nombre):
    print(f"[*] Configurando {nombre}...")
    conexion.send_config_set(comandos)
    conexion.save_config()
    print(f"[+] {nombre} listo.")

print("=== Automatización de Red — VPN AnyConnect requerida ===\n")
print("1. Solo Switch")
print("2. Solo Routers")
print("3. Todo")
opcion = input("\nOpción (1-3): ").strip()

conexiones = {}

if opcion in ('1', '3'):
    try:
        c = ConnectHandler(**SWITCH)
        configurar(c, COMANDOS_SWITCH, "Switch Nexus")
        conexiones['switch'] = c
    except Exception as e:
        print(f"[-] Switch: {e}")

if opcion in ('2', '3'):
    try:
        c = ConnectHandler(**ROUTER1)
        configurar(c, COMANDOS_ROUTER1, "Router 1")
        conexiones['r1'] = c
    except Exception as e:
        print(f"[-] Router 1: {e}")

    try:
        c = ConsolaRouter(DEVBOX, puerto=2223, usuario='developer', clave='C1sco12345')
        configurar(c, COMANDOS_ROUTER2, "Router 2")
        conexiones['r2'] = c
    except Exception as e:
        print(f"[-] Router 2: {e}")

# Ping de validación (solo si ambos routers están activos)
if 'r1' in conexiones and 'r2' in conexiones:
    print("\n[*] Validando conectividad (ping R2 → R1)...")
    time.sleep(5)
    resultado = conexiones['r2'].send_command("ping 192.168.10.1 source GigabitEthernet1.10")
    print(resultado)

for c in conexiones.values():
    c.disconnect()

print("\n¡Listo!")
