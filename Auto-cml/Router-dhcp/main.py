from netmiko import ConnectHandler, redispatch
import time
from config import (
    CML_HOST, CML_USER, CML_PASS, ENABLE_SECRET,
    CONSOLA_R1, CONSOLA_SW1,
    COMANDOS_R1, COMANDOS_SW1,
)


def configurar(consola, comandos, nombre):
    print(f"\n[*] Conectando a {nombre}...")
    con = ConnectHandler(
        device_type="generic_termserver",
        host=CML_HOST,
        username=CML_USER,
        password=CML_PASS,
    )
    try:
        con.write_channel(f"open {consola}\n")
        for espera in (4, 2, 2):
            time.sleep(espera)
            con.write_channel("\n")
        con.read_channel()

        redispatch(con, device_type="cisco_ios")
        con.secret = ENABLE_SECRET
        con.enable()

        print("[+] Comandos:")
        print("\n".join(comandos))
        con.send_config_set(comandos)
        con.save_config()
        print(f"[OK] {nombre} configurado y guardado.")
    finally:
        con.disconnect()


print("=== Router DHCP - VPN requerida ===\n")
print("1. Router (R1)")
print("2. Switch (SW1)")

opcion = input("\nOpcion (1-2): ").strip()

if opcion == "1":
    configurar(CONSOLA_R1, COMANDOS_R1, "Router R1")
elif opcion == "2":
    configurar(CONSOLA_SW1, COMANDOS_SW1, "Switch SW1")
else:
    print("\nOpcion invalida. Debe ser 1 o 2.")

print("\nListo!")
