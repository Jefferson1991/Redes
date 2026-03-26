# ============================================================
# main.py — Menú principal (Switch + Routers)
# ============================================================
# Ejecutar: python main.py
# Requisito: VPN AnyConnect del sandbox activa

import sys
from switch import configurar_switch
from routers import conectar_router1, conectar_router2, configurar, validar_ping
from config import COMANDOS_ROUTER1, COMANDOS_ROUTER2


def main():
    print("=== Automatización de Infraestructura de Red ===")
    print("REQUISITO: VPN AnyConnect del sandbox activa.\n")
    print("¿Qué desea configurar?")
    print("  1. Solo Switch Nexus 9K       → python switch.py")
    print("  2. Solo Routers (R1 y R2)     → python routers.py")
    print("  3. Todo (Switch + Routers + ping de validación)")

    opcion = input("\nSeleccione opción (1-3): ").strip()

    if opcion == '1':
        configurar_switch()

    elif opcion == '2':
        r1 = conectar_router1()
        r2 = conectar_router2()
        if r1:
            configurar(r1, "Router 1", COMANDOS_ROUTER1)
        if r2:
            configurar(r2, "Router 2", COMANDOS_ROUTER2)
        if r1 and r2:
            validar_ping(r2)
        if r1:
            r1.disconnect()
        if r2:
            r2.disconnect()

    elif opcion == '3':
        configurar_switch()
        r1 = conectar_router1()
        r2 = conectar_router2()
        if r1:
            configurar(r1, "Router 1", COMANDOS_ROUTER1)
        if r2:
            configurar(r2, "Router 2", COMANDOS_ROUTER2)
        if r1 and r2:
            validar_ping(r2)
        if r1:
            r1.disconnect()
        if r2:
            r2.disconnect()

    else:
        print("[-] Opción inválida. Saliendo...")
        sys.exit(1)

    print("\n¡Despliegue finalizado exitosamente!")


if __name__ == '__main__':
    main()
