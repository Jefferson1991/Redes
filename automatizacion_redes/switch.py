# ============================================================
# switch.py — Configura solo el Switch Nexus 9K
# ============================================================
# Ejecutar: python switch.py
# Requisito: VPN AnyConnect del sandbox activa

from netmiko import ConnectHandler
from config import SWITCH, COMANDOS_SWITCH


def configurar_switch():
    host = SWITCH['params']['host']
    print(f"\n[*] Conectando al Switch Nexus ({host}) via SSH...")

    try:
        conexion = ConnectHandler(**SWITCH['params'])
        print("[+] Conexión establecida.")
    except Exception as e:
        print(f"[-] No se pudo conectar al Switch: {e}")
        return

    print("[*] Enviando comandos de configuración...")
    try:
        conexion.send_config_set(COMANDOS_SWITCH)
        conexion.save_config()
        print("[+] Configuración aplicada y guardada.")
    except Exception as e:
        print(f"[-] Error al configurar el Switch: {e}")

    conexion.disconnect()
    print("[*] Conexión cerrada.")


if __name__ == '__main__':
    print("=== Configuración del Switch Nexus 9K ===")
    print("REQUISITO: VPN AnyConnect activa.\n")
    configurar_switch()
    print("\n¡Listo!")
