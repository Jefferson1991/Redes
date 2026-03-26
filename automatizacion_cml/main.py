from netmiko import ConnectHandler
from config import R1, R2, SW1, SW2
from config import COMANDOS_R1, COMANDOS_R2, COMANDOS_SW1, COMANDOS_SW2
import time

def configurar(params, comandos, nombre):
    print(f"\n[*] Conectando a {nombre} ({params['host']})...")
    try:
        con = ConnectHandler(**params)
        con.enable()
        print(f"[+] Conectado. Enviando comandos...")
        con.send_config_set(comandos)
        con.save_config()
        con.disconnect()
        print(f"[+] {nombre} configurado y guardado.")
    except Exception as e:
        print(f"[-] Error en {nombre}: {e}")

print("=== Automatización CML — VPN requerida ===\n")
print("1. Solo Routers (R1 y R2)")
print("2. Solo Switches (SW1 y SW2)")
print("3. Todo")
opcion = input("\nOpción (1-3): ").strip()

if opcion in ('1', '3'):
    configurar(R1, COMANDOS_R1, "Router 1")
    configurar(R2, COMANDOS_R2, "Router 2")

if opcion in ('2', '3'):
    configurar(SW1, COMANDOS_SW1, "Switch 1")
    configurar(SW2, COMANDOS_SW2, "Switch 2")

print("\n¡Listo!")
