# Requisito: VPN activa antes de ejecutar
#
# Topología CML (sandbox):
#   R1 E0/0 <--> SW1 E0/2 (trunk Router-on-a-Stick)
#   R1 E0/1 <--> R2 E0/2
#   SW1 E0/0 -> PC1 (VLAN 10), SW1 E0/1 -> PC2 (VLAN 20)



R1 = {
    'device_type': 'cisco_ios_telnet',
    'host': '10.10.20.171',
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
# --- Comandos por dispositivo ---
# Interfaces usan Ethernet (no GigabitEthernet) en IOL XE

COMANDOS_R1 = [
    'hostname R1',
    'no ip domain-lookup',
    'banner motd #Acceso solo para personal de TI#',
    'interface Ethernet0/0',
    'no ip address',
    'no shutdown',
    'exit',
    'interface Ethernet0/0.10',
    'encapsulation dot1Q 10',
    'ip address 192.168.20.1 255.255.255.192',
    'description GW_COMPRAS',
    'exit',
    'interface Ethernet0/0.20',
    'encapsulation dot1Q 20',
    'ip address 192.168.20.65 255.255.255.224',
    'description GW_VENTAS',
    'exit',
    'interface Ethernet0/0.99',
    'encapsulation dot1Q 99',
    'ip address 192.168.20.97 255.255.255.252',
    'description GW_GESTION',
    'exit',
]
COMANDOS_SW1 = [
    'hostname SW1',
    'banner motd #Acceso solo para personal de TI#',
    'vlan 10',
    'name COMPRAS',
    'exit',
    'vlan 20',
    'name VENTAS',
    'exit',
    'vlan 99',
    'name GESTION',
    'exit',
    # PC1 / PC2 (según diagrama)
    'interface Ethernet0/0',
    'switchport mode access',
    'switchport access vlan 10',
    'no shutdown',
    'exit',
    'interface Ethernet0/1',
    'switchport mode access',
    'switchport access vlan 20',
    'no shutdown',
    'exit',
    # Trunk hacia R1 E0/0
    'interface Ethernet0/2',
    'switchport trunk encapsulation dot1q',
    'switchport mode trunk',
    'switchport trunk allowed vlan 10,20,99',
    'switchport nonegotiate',
    'no shutdown',
    'exit',
    # Gestión del switch
    'interface vlan 99',
    'ip address 192.168.20.98 255.255.255.252',
    'no shutdown',
    'exit',
    'ip default-gateway 192.168.20.97',
]













































































'''R2 = {
    'device_type': 'cisco_ios_telnet',
    'host': '10.10.20.172',
    'username': 'cisco',
    'password': 'cisco',
    'secret': 'cisco',
}'''

'''SW2 = {
    'device_type': 'cisco_ios_telnet',
    'host': '10.10.20.174',
    'username': 'cisco',
    'password': 'cisco',
    'secret': 'cisco',
}'''

'''COMANDOS_SW2 = [
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
]'''