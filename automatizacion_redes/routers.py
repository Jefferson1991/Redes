# ============================================================
# routers.py — Configura Router 1 y Router 2
# ============================================================
# Ejecutar: python routers.py
# Requisito: VPN AnyConnect del sandbox activa
#
# Router 1 (Cat8k-1): SSH directo al host 10.10.20.48
# Router 2 (Cat8k-2): Acceso via consola serial del DevBox
#   Flujo R2: tu PC → SSH DevBox (10.10.20.50) → telnet puerto 2223

import time
from netmiko import ConnectHandler
from consola_router import ConsolaRouter
from config import DEVBOX, ROUTER1, ROUTER2, COMANDOS_ROUTER1, COMANDOS_ROUTER2


def conectar_router1():
    host = ROUTER1['params']['host']
    print(f"\n[*] Conectando a Router 1 ({host}) via SSH directo...")
    try:
        conexion = ConnectHandler(**ROUTER1['params'])
        print("[+] Router 1 conectado.")
        return conexion
    except Exception as e:
        print(f"[-] Error al conectar Router 1: {e}")
        return None


def conectar_router2():
    print("\n[*] Conectando a Router 2 via consola del DevBox...")
    try:
        conexion = ConsolaRouter(
            DEVBOX,
            ROUTER2['console_port'],
            ROUTER2['router_user'],
            ROUTER2['router_pass']
        )
        print("[+] Router 2 conectado.")
        return conexion
    except Exception as e:
        print(f"[-] Error al conectar Router 2: {e}")
        return None


def configurar(conexion, nombre, comandos):
    print(f"[*] Enviando comandos a {nombre}...")
    try:
        conexion.send_config_set(comandos)
        conexion.save_config()
        print(f"[+] {nombre} configurado y guardado.")
    except Exception as e:
        print(f"[-] Error al configurar {nombre}: {e}")


def validar_ping(conexion_r2):
    """Ping desde R2 (192.168.10.2) hacia R1 (192.168.10.1) para comprobar conectividad."""
    print("\n[*] Esperando 5 segundos para convergencia de red...")
    time.sleep(5)
    print("[*] Ping desde Router 2 → Router 1...")
    resultado = conexion_r2.send_command(
        "ping 192.168.10.1 source GigabitEthernet1.10",
        read_timeout=15
    )
    print("\n--- Resultado del Ping ---")
    print(resultado)
    print("--------------------------")


if __name__ == '__main__':
    print("=== Configuración de Routers (R1 y R2) ===")
    print("REQUISITO: VPN AnyConnect activa.\n")

    r1 = conectar_router1()
    r2 = conectar_router2()

    if r1:
        configurar(r1, "Router 1", COMANDOS_ROUTER1)

    if r2:
        configurar(r2, "Router 2", COMANDOS_ROUTER2)

    # Validación de conectividad entre routers (solo si ambos están activos)
    if r1 and r2:
        validar_ping(r2)

    if r1:
        r1.disconnect()
        print("[*] Router 1 desconectado.")
    if r2:
        r2.disconnect()
        print("[*] Router 2 desconectado.")

    print("\n¡Listo!")
