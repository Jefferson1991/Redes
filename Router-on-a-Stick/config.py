# Router-on-a-Stick — config.py
#
# Conexion via CML Console Server (SSH a 10.10.20.161)
# VPN activa antes de ejecutar.
#
# VLSM base: 192.168.50.0/24
#   Compras    192.168.50.0/26   GW .1    (62 hosts)
#   Ventas     192.168.50.64/27  GW .65   (30 hosts)
#   Inventario 192.168.50.96/28  GW .97   (14 hosts)
#   Gestion    192.168.50.112/30 GW .113  (2 hosts)

# ── CML Console Server ──
CML_HOST = '10.10.20.161'
CML_USER = 'developer'
CML_PASS = 'C1sco12345'
ENABLE_SECRET = 'cisco'

# Rutas de consola: /NombreLab/NombreNodo/Linea
CONSOLA_R1  = '/Examen/cat8000v-0/0'
CONSOLA_SW1 = '/Examen/iosvl2-0/0'
CONSOLA_PC1 = '/Examen/desktop-1/0'
CONSOLA_PC2 = '/Examen/desktop-0/0'

# ── ROUTER R1 ──
# Topologia: R1 GigabitEthernet1 <--> SW1 Gi0/0 (trunk)
COMANDOS_R1 = [
    'hostname R1',
    'no ip domain-lookup',
    'banner motd #Acceso solo para personal de TI#',

    # Interfaz fisica (trunk)
    'interface GigabitEthernet1',
    'no ip address',
    'no shutdown',
    'exit',

    # VLAN 10 - Compras
    'interface GigabitEthernet1.10',
    'encapsulation dot1Q 10',
    'ip address 192.168.50.1 255.255.255.192',
    'description GW_COMPRAS',
    'exit',

    # VLAN 20 - Ventas
    'interface GigabitEthernet1.20',
    'encapsulation dot1Q 20',
    'ip address 192.168.50.65 255.255.255.224',
    'description GW_VENTAS',
    'exit',

    # VLAN 30 - Inventario
    'interface GigabitEthernet1.30',
    'encapsulation dot1Q 30',
    'ip address 192.168.50.97 255.255.255.240',
    'description GW_INVENTARIO',
    'exit',

    # VLAN 99 - Gestion
    'interface GigabitEthernet1.99',
    'encapsulation dot1Q 99',
    'ip address 192.168.50.113 255.255.255.252',
    'description GW_GESTION',
    'exit',
]

# ── SWITCH SW1 ──
# Topologia:
#   SW1 Gi0/0 <--> R1 G1       (trunk)
#   SW1 Gi0/1 <--> desktop-1   (VLAN 10)
#   SW1 Gi0/2 <--> desktop-0   (VLAN 20)
COMANDOS_SW1 = [
    'hostname SW1',
    'banner motd #Acceso solo para personal de TI#',

    # Crear VLANs
    'vlan 10', 'name COMPRAS', 'exit',
    'vlan 20', 'name VENTAS', 'exit',
    'vlan 30', 'name INVENTARIO', 'exit',
    'vlan 99', 'name GESTION', 'exit',

    # Access: desktop-1 -> VLAN 10
    'interface GigabitEthernet0/1',
    'switchport mode access',
    'switchport access vlan 10',
    'no shutdown', 'exit',

    # Access: desktop-0 -> VLAN 20
    'interface GigabitEthernet0/2',
    'switchport mode access',
    'switchport access vlan 20',
    'no shutdown', 'exit',

    # Trunk hacia R1
    'interface GigabitEthernet0/0',
    'switchport trunk encapsulation dot1q',
    'switchport mode trunk',
    'switchport trunk allowed vlan 10,20,30,99',
    'switchport nonegotiate',
    'no shutdown', 'exit',

    # SVI gestion
    'interface vlan 99',
    'ip address 192.168.50.114 255.255.255.252',
    'no shutdown', 'exit',
    'ip default-gateway 192.168.50.113',
]

# ── HOSTS LINUX (Alpine) ──
# Necesitan sudo su antes (el script lo maneja)
COMANDOS_PC1 = [
    'ip addr add 192.168.50.2/26 dev eth0',
    'ip route add default via 192.168.50.1',
]

COMANDOS_PC2 = [
    'ip addr add 192.168.50.66/27 dev eth0',
    'ip route add default via 192.168.50.65',
]
