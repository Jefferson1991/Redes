# Requisito: VPN activa antes de ejecutar

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

COMANDOS_R1 = [
    'banner motd #Acceso solo para personal de TI#',
    'no ip domain-lookup',
    'interface GigabitEthernet0/0',
    'ip address 192.168.10.1 255.255.255.0',
    'no shutdown',
]

COMANDOS_R2 = [
    'banner motd #Acceso solo para personal de TI#',
    'no ip domain-lookup',
    'interface GigabitEthernet0/0',
    'ip address 192.168.10.2 255.255.255.0',
    'no shutdown',
]

COMANDOS_SW1 = [
    'banner motd #Acceso solo para personal de TI#',
    'vlan 10',
    'name VLAN_DATOS',
    'exit',
    'interface range GigabitEthernet0/0 - 1',
    'switchport mode trunk',
    'switchport trunk allowed vlan 10',
    'no shutdown',
]

COMANDOS_SW2 = [
    'banner motd #Acceso solo para personal de TI#',
    'vlan 10',
    'name VLAN_DATOS',
    'exit',
    'interface range GigabitEthernet0/0 - 1',
    'switchport mode trunk',
    'switchport trunk allowed vlan 10',
    'no shutdown',
]
