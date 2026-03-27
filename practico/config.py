

r1 = {  
    'device_type': 'cisco_ios',
    'host': '192.168.1.1',
    'username': 'admin',
    'password': 'password',
    'secret': 'password'
}

sw1 = {
    'device_type': 'cisco_ios',
    'host': '192.168.1.2',
    'username': 'admin',
    'password': 'password',
    'secret': 'password'
}

##comandos para configurar los routers y switches

comandos_r1 = [
    'hostname R1', 
    'interface fa0/0',
    'ip address 192.168.1.1 255.255.255.0',
    'no shutdown'
]

comandos_sw1 = [
    'hostname SW1',
    'interface fa0/1',
    'switchport mode access',
    'switchport access vlan 10'
]