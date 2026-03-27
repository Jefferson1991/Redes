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
    'hostname R1',  # Nombre del router
    'no ip domain-lookup',  # Evita espera por DNS
    'banner motd #Acceso solo para personal de TI#',  # Banner legal
    'service password-encryption',  # Cifra passwords en running-config
    'enable secret cisco',  # Clave de modo privilegiado
    'username cisco privilege 15 secret cisco',  # Usuario admin local
    'line con 0',  # Entra a consola local
    'password cisco',  # Clave de consola
    'login',  # Exige login por consola
    'exit',  # Sale de line con
    'line vty 0 4',  # Entra a lineas remotas
    'login local',  # Usa usuario local en VTY
    'transport input ssh telnet',  # Permite SSH/Telnet remoto
    'exit',  # Sale de line vty

    # Interfaz fisica (trunk)
    'interface GigabitEthernet1',  # Interfaz fisica hacia SW1
    'no ip address',  # Sin IP en interfaz madre
    'no shutdown',  # Activa interfaz fisica
    'exit',  # Sale de interfaz fisica

    # VLAN 10 - Compras
    'interface GigabitEthernet1.10',  # Subinterfaz VLAN 10
    'encapsulation dot1Q 10',  # Etiqueta trafico VLAN 10
    'ip address 192.168.50.1 255.255.255.192',  # Gateway VLAN 10
    'description GW_COMPRAS',  # Descripcion de interfaz
    'exit',  # Sale de subinterfaz

    # VLAN 20 - Ventas
    'interface GigabitEthernet1.20',  # Subinterfaz VLAN 20
    'encapsulation dot1Q 20',  # Etiqueta trafico VLAN 20
    'ip address 192.168.50.65 255.255.255.224',  # Gateway VLAN 20
    'description GW_VENTAS',  # Descripcion de interfaz
    'exit',  # Sale de subinterfaz

    # VLAN 30 - Inventario
    'interface GigabitEthernet1.30',  # Subinterfaz VLAN 30
    'encapsulation dot1Q 30',  # Etiqueta trafico VLAN 30
    'ip address 192.168.50.97 255.255.255.240',  # Gateway VLAN 30
    'description GW_INVENTARIO',  # Descripcion de interfaz
    'exit',  # Sale de subinterfaz

    # VLAN 99 - Gestion
    'interface GigabitEthernet1.99',  # Subinterfaz VLAN 99
    'encapsulation dot1Q 99',  # Etiqueta trafico VLAN 99
    'ip address 192.168.50.113 255.255.255.252',  # Gateway gestion
    'description GW_GESTION',  # Descripcion de interfaz
    'exit',  # Sale de subinterfaz
]

# ── SWITCH SW1 ──
# Topologia:
#   SW1 Gi0/0 <--> R1 G1       (trunk)
#   SW1 Gi0/1 <--> desktop-1   (VLAN 10)
#   SW1 Gi0/2 <--> desktop-0   (VLAN 20)
COMANDOS_SW1 = [
    'hostname SW1',  # Nombre del switch
    'banner motd #Acceso solo para personal de TI#',  # Banner legal
    'service password-encryption',  # Cifra passwords en running-config
    'enable secret cisco',  # Clave de modo privilegiado
    'username cisco privilege 15 secret cisco',  # Usuario admin local
    'line con 0',  # Entra a consola local
    'password cisco',  # Clave de consola
    'login',  # Exige login por consola
    'exit',  # Sale de line con
    'line vty 0 4',  # Entra a lineas remotas
    'login local',  # Usa usuario local en VTY
    'transport input ssh telnet',  # Permite SSH/Telnet remoto
    'exit',  # Sale de line vty

    # Crear VLANs
    'vlan 10',  # Crea VLAN 10
    'name COMPRAS',  # Nombra VLAN 10
    'exit',  # Sale de vlan 10
    'vlan 20',  # Crea VLAN 20
    'name VENTAS',  # Nombra VLAN 20
    'exit',  # Sale de vlan 20
    'vlan 30',  # Crea VLAN 30
    'name INVENTARIO',  # Nombra VLAN 30
    'exit',  # Sale de vlan 30
    'vlan 99',  # Crea VLAN 99
    'name GESTION',  # Nombra VLAN 99
    'exit',  # Sale de vlan 99

    # Access: desktop-1 -> VLAN 10
    'interface GigabitEthernet0/1',  # Puerto a PC1
    'switchport mode access',  # Fuerza modo access
    'switchport access vlan 10',  # Asigna VLAN 10
    'no shutdown',  # Activa puerto
    'exit',  # Sale de interfaz

    # Access: desktop-0 -> VLAN 20
    'interface GigabitEthernet0/2',  # Puerto a PC2
    'switchport mode access',  # Fuerza modo access
    'switchport access vlan 20',  # Asigna VLAN 20
    'no shutdown',  # Activa puerto
    'exit',  # Sale de interfaz

    # Trunk hacia R1
    'interface GigabitEthernet0/0',  # Puerto trunk a R1
    'switchport trunk encapsulation dot1q',  # Encapsulacion trunk
    'switchport mode trunk',  # Fuerza modo trunk
    'switchport trunk allowed vlan 10,20,30,99',  # VLANs permitidas
    'switchport nonegotiate',  # Desactiva DTP
    'no shutdown',  # Activa trunk
    'exit',  # Sale de interfaz

    # SVI gestion
    'interface vlan 99',  # SVI de gestion
    'ip address 192.168.50.114 255.255.255.252',  # IP de gestion SW1
    'no shutdown',  # Activa SVI
    'exit',  # Sale de SVI
    'ip default-gateway 192.168.50.113',  # Gateway de gestion
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
