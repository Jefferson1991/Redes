from netmiko import ConnectHandler
from config import R1, SW1, COMANDOS_R1, COMANDOS_SW1


def configurar(params, comandos, nombre):
    print(f"\n[*] Conectando a {nombre} ({params['host']})...")
    try:
        with ConnectHandler(**params) as con:
            con.enable()
            print("[+] Comandos a enviar:")
            print("\n".join(comandos))
            con.send_config_set(comandos)
            con.save_config()
        print(f"[+] {nombre} configurado y guardado.")
    except Exception as e:
        print(f"[-] Error en {nombre}: {e}")


print("=== Router-on-a-Stick - VPN requerida ===\n")
print("1. Solo Router (R1)")
print("2. Solo Switch (SW1)")
print("3. Todo")

opcion = input("\nOpción (1-3): ").strip()

if opcion in ("1", "3"):
    configurar(R1, COMANDOS_R1, "Router 1")

if opcion in ("2", "3"):
    configurar(SW1, COMANDOS_SW1, "Switch 1")

print("\n¡Listo!")

