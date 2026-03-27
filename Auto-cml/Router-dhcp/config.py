# Router-dhcp — config.py
#
# Laboratorio base para practicar DHCP en router Cisco via CML Console Server.

# ── CML Console Server ──
CML_HOST = '10.10.20.161'
CML_USER = 'developer'
CML_PASS = 'C1sco12345'
ENABLE_SECRET = 'cisco'

# Rutas de consola (ajusta el nombre de lab/nodo si cambia)
CONSOLA_R1 = '/Examen/cat8000v-0/0'
CONSOLA_SW1 = '/Examen/iosvl2-0/0'

# ── ROUTER R1 ──
# Escenario:
#   VLAN 10 -> 192.168.10.0/24  (gateway .1)
#   VLAN 20 -> 192.168.20.0/24  (gateway .1)
# DHCP entregado desde el router.
COMANDOS_R1 = [
    'hostname R1',  # Nombre del router
    'no ip domain-lookup',  # Evita espera por DNS
    'banner motd #Acceso solo para personal de TI#',  # Banner legal
    'service password-encryption',  # Cifra passwords visibles
    'enable secret cisco',  # Clave de modo enable
    'username cisco privilege 15 secret cisco',  # Usuario admin local
    'line con 0',  # Consola local
    'password cisco',  # Clave consola
    'login',  # Exigir login en consola
    'exit',  # Salir de line con
    'line vty 0 4',  # Líneas remotas
    'login local',  # Login por usuario local
    'transport input ssh telnet',  # Permite SSH/Telnet
    'exit',  # Salir de line vty

    'interface GigabitEthernet1',  # Interfaz física al switch
    'no ip address',  # Sin IP en interfaz madre
    'no shutdown',  # Activar enlace físico
    'exit',  # Salir de interfaz

    'interface GigabitEthernet1.10',  # Subif VLAN 10
    'encapsulation dot1Q 10',  # Etiqueta VLAN 10
    'ip address 192.168.10.1 255.255.255.0',  # Gateway VLAN 10
    'description GW_VLAN10',  # Descripción
    'exit',  # Salir de subif

    'interface GigabitEthernet1.20',  # Subif VLAN 20
    'encapsulation dot1Q 20',  # Etiqueta VLAN 20
    'ip address 192.168.20.1 255.255.255.0',  # Gateway VLAN 20
    'description GW_VLAN20',  # Descripción
    'exit',  # Salir de subif

    'ip dhcp excluded-address 192.168.10.1 192.168.10.20',  # Reservar rango estático VLAN 10
    'ip dhcp excluded-address 192.168.20.1 192.168.20.20',  # Reservar rango estático VLAN 20

    'ip dhcp pool VLAN10',  # Pool DHCP VLAN 10
    'network 192.168.10.0 255.255.255.0',  # Red del pool
    'default-router 192.168.10.1',  # Gateway entregado por DHCP
    'dns-server 8.8.8.8',  # DNS entregado por DHCP
    'exit',  # Salir de pool

    'ip dhcp pool VLAN20',  # Pool DHCP VLAN 20
    'network 192.168.20.0 255.255.255.0',  # Red del pool
    'default-router 192.168.20.1',  # Gateway entregado por DHCP
    'dns-server 8.8.8.8',  # DNS entregado por DHCP
    'exit',  # Salir de pool
]

# ── SWITCH SW1 ──
COMANDOS_SW1 = [
    'hostname SW1',  # Nombre del switch
    'banner motd #Acceso solo para personal de TI#',  # Banner legal
    'service password-encryption',  # Cifra passwords visibles
    'enable secret cisco',  # Clave de modo enable
    'username cisco privilege 15 secret cisco',  # Usuario admin local
    'line con 0',  # Consola local
    'password cisco',  # Clave consola
    'login',  # Exigir login en consola
    'exit',  # Salir de line con
    'line vty 0 4',  # Líneas remotas
    'login local',  # Login por usuario local
    'transport input ssh telnet',  # Permite SSH/Telnet
    'exit',  # Salir de line vty

    'vlan 10',  # Crear VLAN 10
    'name USUARIOS_A',  # Nombre VLAN 10
    'exit',  # Salir de VLAN 10
    'vlan 20',  # Crear VLAN 20
    'name USUARIOS_B',  # Nombre VLAN 20
    'exit',  # Salir de VLAN 20

    'interface GigabitEthernet0/1',  # Puerto host VLAN 10
    'switchport mode access',  # Modo access
    'switchport access vlan 10',  # Asignar VLAN 10
    'no shutdown',  # Activar puerto
    'exit',  # Salir de interfaz

    'interface GigabitEthernet0/2',  # Puerto host VLAN 20
    'switchport mode access',  # Modo access
    'switchport access vlan 20',  # Asignar VLAN 20
    'no shutdown',  # Activar puerto
    'exit',  # Salir de interfaz

    'interface GigabitEthernet0/0',  # Trunk al router
    'switchport trunk encapsulation dot1q',  # Encapsulación trunk
    'switchport mode trunk',  # Modo trunk
    'switchport trunk allowed vlan 10,20',  # VLANs permitidas
    'switchport nonegotiate',  # Sin negociación DTP
    'no shutdown',  # Activar trunk
    'exit',  # Salir de interfaz
]

# ── HOSTS LINUX (OPCIONAL) ──
# No requieren IP fija: solo pedir IP por DHCP.
COMANDOS_PC1 = [
    'sudo su',  # Escalar a root
    'dhclient -r eth0',  # Liberar lease anterior
    'dhclient -v eth0',  # Pedir IP por DHCP
    'ip addr show eth0',  # Ver IP recibida
    'ip route',  # Ver gateway por defecto
]

COMANDOS_PC2 = [
    'sudo su',  # Escalar a root
    'dhclient -r eth0',  # Liberar lease anterior
    'dhclient -v eth0',  # Pedir IP por DHCP
    'ip addr show eth0',  # Ver IP recibida
    'ip route',  # Ver gateway por defecto
]
