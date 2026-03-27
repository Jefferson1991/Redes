# Plantilla para Router-on-a-Stick (completar con tu VLSM)
#
# Requisito: VPN activa antes de ejecutar.
#
# Hosts (puedes ajustarlos si cambian):

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

# =========================
# COMANDOS PARA EL ROUTER R1
# =========================
#
# Usa subinterfaces Ethernet0/0.<vlan> y encapsulación dot1Q.
# Completa las IPs/Máscaras según tu plan VLSM.
#
COMANDOS_R1 = [
    'hostname R1',  # Define el nombre del router
    'no ip domain-lookup',  # Desactiva la búsqueda DNS por nombre
    'banner motd #Acceso solo para personal de TI#',  # Mensaje legal en consola

    # Limpia IP de la interfaz física (las subinterfaces llevarán la IP)
    'interface Ethernet0/0',  # Entra a la interfaz física
    'no ip address',  # Sin IP en la interfaz física (solo subinterfaces)
    'no shutdown',  # Activa la interfaz física
    'exit',  # Sale de la interfaz

    # VLAN 10 (Compras)
    'interface Ethernet0/0.10',  # Subinterfaz VLAN 10 (Compras)
    'encapsulation dot1Q 10',  # Etiqueta frames para VLAN 10
    'ip address 192.168.50.1 255.255.255.192',  # Gateway VLAN 10
    'description GW_COMPRAS',  # Descripción del gateway
    'exit',  # Sale de la subinterfaz

    # VLAN 20 (Ventas)
    'interface Ethernet0/0.20',  # Subinterfaz VLAN 20 (Ventas)
    'encapsulation dot1Q 20',  # Etiqueta frames para VLAN 20
    'ip address 192.168.50.65 255.255.255.224',  # Gateway VLAN 20
    'description GW_VENTAS',  # Descripción del gateway
    'exit',  # Sale de la subinterfaz

    # VLAN 30 (Inventario)
    'interface Ethernet0/0.30',  # Subinterfaz VLAN 30 (Inventario)
    'encapsulation dot1Q 30',  # Etiqueta frames para VLAN 30
    'ip address 192.168.50.97 255.255.255.240',  # Gateway VLAN 30
    'description GW_INVENTARIO',  # Descripción del gateway
    'exit',  # Sale de la subinterfaz

    # VLAN 99 (Gestión)
    'interface Ethernet0/0.99',  # Subinterfaz VLAN 99 (Gestión)
    'encapsulation dot1Q 99',  # Etiqueta frames para VLAN 99
    'ip address 192.168.50.113 255.255.255.252',  # Gateway VLAN 99
    'description GW_GESTION',  # Descripción del gateway
    'exit',  # Sale de la subinterfaz
]

# =========================
# COMANDOS PARA EL SWITCH SW1
# =========================
#
# Topología CML (según diagrama del lab):
#   R1 E0/0  <-->  SW1 E0/2   (trunk Router-on-a-Stick)
#   SW1 E0/0 <-->  PC1        (access VLAN 10)
#   SW1 E0/1 <-->  PC2        (access VLAN 20)
#   SW1 E0/3     gestión CML  (no usar como access de datos si ya está en mgmt)
#
# - Crea VLAN 10/20/30/99
# - Trunk en Ethernet0/2 hacia R1 (no en E0/0)
# - E0/0/E0/1 access para PC1/PC2
# - SVI VLAN 99 para IP del switch en la red de gestión
#
COMANDOS_SW1 = [
    'hostname SW1',  # Define el nombre del switch
    'banner motd #Acceso solo para personal de TI#',  # Mensaje legal en consola

    'vlan 10',  # Crea VLAN 10
    'name COMPRAS',  # Nombre de la VLAN 10
    'exit',  # Sale de modo VLAN
    'vlan 20',  # Crea VLAN 20
    'name VENTAS',  # Nombre de la VLAN 20
    'exit',  # Sale de modo VLAN
    'vlan 30',  # Crea VLAN 30
    'name INVENTARIO',  # Nombre de la VLAN 30
    'exit',  # Sale de modo VLAN
    'vlan 99',  # Crea VLAN 99
    'name GESTION',  # Nombre de la VLAN 99
    'exit',  # Sale de modo VLAN

    # PC1 (diagrama: E0/0 -> VLAN 10)
    'interface Ethernet0/0',  # Puerto hacia PC1
    'switchport mode access',  # Define modo access
    'switchport access vlan 10',  # VLAN Compras
    'no shutdown',  # Activa el puerto
    'exit',  # Sale del puerto

    # PC2 (diagrama: E0/1 -> VLAN 20)
    'interface Ethernet0/1',  # Puerto hacia PC2
    'switchport mode access',  # Define modo access
    'switchport access vlan 20',  # VLAN Ventas
    'no shutdown',  # Activa el puerto
    'exit',  # Sale del puerto

    # Trunk hacia R1 E0/0 (diagrama: SW1 E0/2 <--> R1 E0/0)
    'interface Ethernet0/2',  # Puerto físico hacia el router (Router-on-a-Stick)
    'switchport trunk encapsulation dot1q',  # Encapsulación del trunk
    'switchport mode trunk',  # Cambia el puerto a trunk
    'switchport trunk allowed vlan 10,20,30,99',  # VLANs permitidas en el trunk
    'switchport nonegotiate',  # Evita negociación DTP
    'no shutdown',  # Activa el trunk
    'exit',  # Sale del puerto

    # Gestión del switch (SVI)
    'interface vlan 99',  # SVI para administración en VLAN 99
    'ip address 192.168.50.114 255.255.255.252',  # IP del switch en VLAN 99
    'no shutdown',  # Activa la SVI
    'exit',  # Sale de la SVI
    'ip default-gateway 192.168.50.113',  # Gateway para tráfico de gestión del switch
]

# =========================
# COMANDOS DE VALIDACION
# (Guia de comprobacion: al lado va la definicion corta)
# =========================

COMANDOS_VALIDACION_R1 = [
    'show ip interface brief',  # Resume interfaces y subinterfaces (up/down + IP)
    'show running-config interface Ethernet0/0.10',  # Verifica IP/mask/VLAN de subinterfaz .10
    'show running-config interface Ethernet0/0.20',  # Verifica IP/mask/VLAN de subinterfaz .20
    'show running-config interface Ethernet0/0.30',  # Verifica IP/mask/VLAN de subinterfaz .30
    'show running-config interface Ethernet0/0.99',  # Verifica IP/mask/VLAN de subinterfaz .99
]

COMANDOS_VALIDACION_SW1 = [
    'show vlan brief',  # Muestra VLANs creadas y puertos asignados
    'show interfaces trunk',  # Confirma el puerto trunk y VLANs permitidas
    'show ip interface brief',  # Confirma SVI VLAN 99 (up/up + IP)
    'ping 192.168.50.113',  # Ping al gateway del router en VLAN 99
    'ping 192.168.50.1',  # Ping al gateway del router en VLAN 10
    'ping 192.168.50.65',  # Ping al gateway del router en VLAN 20
    'ping 192.168.50.97',  # Ping al gateway del router en VLAN 30
]
