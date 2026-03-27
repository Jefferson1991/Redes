from netmiko import ConnectHandler, redispatch
import time
from config import (
    CML_HOST, CML_USER, CML_PASS, ENABLE_SECRET,
    CONSOLA_R1, CONSOLA_SW1,
    COMANDOS_R1, COMANDOS_SW1,
)


def configurar(consola, comandos, nombre):
    print(f'\n[*] Conectando a {nombre}...')

    # 1. Conectar al CML Console Server
    con = ConnectHandler(
        device_type='generic_termserver',
        host=CML_HOST,
        username=CML_USER,
        password=CML_PASS,
    )

    # 2. Abrir consola del dispositivo
    con.write_channel(f'open {consola}\n')
    time.sleep(4)
    con.write_channel('\n')
    time.sleep(2)
    con.write_channel('\n')
    time.sleep(2)
    con.read_channel()  # limpiar buffer

    # 3. Cambiar a modo Cisco IOS
    redispatch(con, device_type='cisco_ios')
    con.secret = ENABLE_SECRET

    # 4. Configurar
    con.enable()
    print('[+] Comandos:')
    print('\n'.join(comandos))
    con.send_config_set(comandos)
    con.save_config()
    con.disconnect()
    print(f'[OK] {nombre} configurado y guardado.')


print('=== Router-on-a-Stick - VPN requerida ===\n')
print('1. Solo Router (R1)')
print('2. Solo Switch (SW1)')
print('3. Todo')

opcion = input('\nOpcion (1-3): ').strip()

if opcion in ('1', '3'):
    configurar(CONSOLA_R1, COMANDOS_R1, 'Router R1')
if opcion in ('2', '3'):
    configurar(CONSOLA_SW1, COMANDOS_SW1, 'Switch SW1')

print('\nListo!')
