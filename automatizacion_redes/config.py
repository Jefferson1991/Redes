# ============================================================
# config.py — Credenciales y comandos de configuración
# ============================================================
# Este es el único archivo que necesitas cambiar para adaptar
# el script a otro laboratorio o dispositivo.

# ------------------------------------------------------------
# DevBox: máquina intermedia para acceder a Router 2 via consola
# ------------------------------------------------------------
DEVBOX = {
    'host': '10.10.20.50',
    'username': 'developer',
    'password': 'C1sco12345',
}

# ------------------------------------------------------------
# Dispositivos: parámetros de conexión
# ------------------------------------------------------------
SWITCH = {
    'tipo': 'netmiko',
    'params': {
        'device_type': 'cisco_nxos',
        'host': '10.10.20.40',
        'username': 'admin',
        'password': 'RG!_Yw200',
        'global_delay_factor': 2,
    }
}

ROUTER1 = {
    'tipo': 'netmiko',
    'params': {
        'device_type': 'cisco_ios',
        'host': '10.10.20.48',          # Cat8k-1 — SSH directo
        'username': 'developer',
        'password': 'C1sco12345',
        'global_delay_factor': 2,
    }
}

ROUTER2 = {
    'tipo': 'consola',                  # Cat8k-2 — via consola del DevBox
    'console_port': 2223,
    'router_user': 'developer',
    'router_pass': 'C1sco12345',
}

# ------------------------------------------------------------
# Comandos de configuración por dispositivo
# ------------------------------------------------------------
COMANDOS_SWITCH = [
    'banner motd #ADVERTENCIA: Acceso autorizado únicamente a personal de TI#',
    'vlan 10',
    'name VLAN_COMPARTIDA',
    'exit',
    'interface Ethernet1/1',
    'switchport',
    'switchport mode trunk',
    'switchport trunk allowed vlan 10',
    'no shutdown',
    'interface Ethernet1/2',
    'switchport',
    'switchport mode trunk',
    'switchport trunk allowed vlan 10',
    'no shutdown',
]

COMANDOS_ROUTER1 = [
    'banner motd #ADVERTENCIA: Acceso autorizado únicamente a personal de TI#',
    'service password-encryption',
    'no ip domain-lookup',
    'ip ssh version 2',
    'ip ssh authentication-retries 3',
    'ip ssh time-out 60',
    'line vty 0 4',
    'exec-timeout 5 0',
    'transport input ssh',
    'exit',
    'interface GigabitEthernet2',
    'no shutdown',
    'interface GigabitEthernet2.10',
    'encapsulation dot1Q 10',
    'ip address 192.168.10.1 255.255.255.0',
    'no shutdown',
]

COMANDOS_ROUTER2 = [
    # Cat8k-pod02 solo tiene GigabitEthernet1 (una sola NIC en QEMU)
    'service password-encryption',
    'no ip domain-lookup',
    'interface GigabitEthernet1',
    'no shutdown',
    'interface GigabitEthernet1.10',
    'encapsulation dot1Q 10',
    'ip address 192.168.10.2 255.255.255.0',
    'no shutdown',
]
