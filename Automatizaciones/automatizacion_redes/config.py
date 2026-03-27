from netmiko import ConnectHandler

# Credenciales de los dispositivos
SWITCH = {
    'device_type': 'cisco_nxos',
    'host': '10.10.20.40',
    'username': 'admin',
    'password': 'RG!_Yw200',
    'global_delay_factor': 2,
}

ROUTER1 = {
    'device_type': 'cisco_ios',
    'host': '10.10.20.48',
    'username': 'developer',
    'password': 'C1sco12345',
    'global_delay_factor': 2,
}

DEVBOX = {
    'host': '10.10.20.50',
    'username': 'developer',
    'password': 'C1sco12345',
}

# Comandos a enviar a cada dispositivo
COMANDOS_SWITCH = [
    'banner motd #Acceso solo para personal de TI#',
    'vlan 10',
    'name VLAN_COMPARTIDA',
    'exit',
    'interface Ethernet1/1',
    'switchport mode trunk',
    'switchport trunk allowed vlan 10',
    'no shutdown',
    'interface Ethernet1/2',
    'switchport mode trunk',
    'switchport trunk allowed vlan 10',
    'no shutdown',
]

COMANDOS_ROUTER1 = [
    'banner motd #Acceso solo para personal de TI#',
    'service password-encryption',
    'no ip domain-lookup',
    'ip ssh version 2',
    'interface GigabitEthernet2',
    'no shutdown',
    'interface GigabitEthernet2.10',
    'encapsulation dot1Q 10',
    'ip address 192.168.10.1 255.255.255.0',
    'no shutdown',
]

COMANDOS_ROUTER2 = [
    'service password-encryption',
    'no ip domain-lookup',
    'interface GigabitEthernet1',
    'no shutdown',
    'interface GigabitEthernet1.10',
    'encapsulation dot1Q 10',
    'ip address 192.168.10.2 255.255.255.0',
    'no shutdown',
]
