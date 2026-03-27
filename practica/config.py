HOST = '10.10.20.161'
USERNAME = 'developer'
PASSWORD = 'C1sco12345'
SECRET = 'cisco'


RUTA_CONSOLAR = '/Examen/cat8000v-0/0'
RUTA_CONSOLAS = '/Examen/iosvl2-0/0'

R1_COMANDOS = [
    'hostname R1',
    'no ip domain-lookup',
    'banner motd #Acceso solo para personal de TI#',
    'interface Ethernet0/0',
    'no ip address',
    'no shutdown',
    'exit',
]
SW1_COMANDOS = [
    'hostname SW1',
    'no ip domain-lookup',
    'banner motd #Acceso solo para personal de TI#',
    'interface Ethernet0/0',
    'no ip address',
    'no shutdown',
    'exit',
]




