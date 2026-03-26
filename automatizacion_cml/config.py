# Requisito: VPN activa antes de ejecutar
#
# Topología real del sandbox:
#   R1  — Eth0/0: 10.10.10.100  Eth0/1: 1.1.1.1 (enlace a R2)
#   R2  — Eth0/0: 20.20.20.100  Eth0/1: 1.1.1.2 (enlace a R1)
#   SW1 — Eth0/0: vlan10  Eth0/1: vlan20  Eth0/2: vlan10
#   SW2 — igual que SW1

R1 = {
    'device_type': 'cisco_ios_telnet',
    'host': '10.10.20.171',
    'username': 'cisco',
    'password': 'cisco',
    'secret': 'cisco',
}

R2 = {
    'device_type': 'cisco_ios_telnet',
    'host': '10.10.20.172',
    'username': 'cisco',
    'password': 'cisco',
    'secret': 'cisco',
}

SW1 = {
    'device_type': 'cisco_ios_telnet',
    'host': '10.10.20.173',
    'username': 'cisco',
    'password': 'cisco',
    'secret': 'cisco',
}

SW2 = {
    'device_type': 'cisco_ios_telnet',
    'host': '10.10.20.174',
    'username': 'cisco',
    'password': 'cisco',
    'secret': 'cisco',
}

# --- Comandos por dispositivo ---
# Interfaces usan Ethernet (no GigabitEthernet) en IOL XE

COMANDOS_R1 = [
    'banner motd #Acceso solo para personal de TI#',
    'no ip domain-lookup',
    'ip ssh version 2',
    'line vty 0 4',
    'transport input ssh telnet',
    'exit',
    # Configurar OSPF para llegar a la red de R2
    'router ospf 1',
    'network 10.10.10.0 0.0.0.255 area 0',
    'network 1.1.1.0 0.0.0.255 area 0',
    'exit',
]

COMANDOS_R2 = [
    'banner motd #Acceso solo para personal de TI#',
    'no ip domain-lookup',
    'ip ssh version 2',
    'line vty 0 4',
    'transport input ssh telnet',
    'exit',
    # Configurar OSPF para llegar a la red de R1
    'router ospf 1',
    'network 20.20.20.0 0.0.0.255 area 0',
    'network 1.1.1.0 0.0.0.255 area 0',
    'exit',
]

COMANDOS_SW1 = [
    'banner motd #Acceso solo para personal de TI#',
    'vlan 10',
    'name VLAN_DATOS',
    'exit',
    'vlan 20',
    'name VLAN_VOZ',
    'exit',
    'interface Ethernet0/0',
    'switchport mode access',
    'switchport access vlan 10',
    'no shutdown',
    'interface Ethernet0/1',
    'switchport mode access',
    'switchport access vlan 20',
    'no shutdown',
]

COMANDOS_SW2 = [
    'banner motd #Acceso solo para personal de TI#',
    'vlan 10',
    'name VLAN_DATOS',
    'exit',
    'vlan 20',
    'name VLAN_VOZ',
    'exit',
    'interface Ethernet0/0',
    'switchport mode access',
    'switchport access vlan 10',
    'no shutdown',
    'interface Ethernet0/1',
    'switchport mode access',
    'switchport access vlan 20',
    'no shutdown',
]
