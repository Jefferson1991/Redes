from netmiko import ConnectHandler, redispatch
import time
from config import (HOST, 
                    USERNAME, PASSWORD, SECRET, 
                    RUTA_CONSOLAR, RUTA_CONSOLAS, 
                    R1_COMANDOS, SW1_COMANDOS)

def configurar (consola, comandos, dispositivo):
    print(f"Conectando a {dispositivo}...")
    conexion = ConnectHandler(
        device_type='cisco_ios',
        host=HOST,
        username=USERNAME,
        password=PASSWORD,
        secret=SECRET,
    )
    try:
        conexion.write_channel(f'open {consola}\n')
        for espera in (4,2,2):
            time.sleep(espera)
            conexion.write_channel('\n')
            conexion.read_channel()
        conexion.read_timeout = 60
        redispatch(conexion, device_type='cisco_ios')
        conexion.secret = SECRET
        if not conexion.check_enable_mode():
            conexion.enable()
        print(f'Ejecutando comandos en {dispositivo}...')
        print('\n'.join(comandos))
        conexion.send_config_set(comandos)
        conexion.save_config()
        print(f"Configuración de {dispositivo} completada.")
    finally:
        conexion.disconnect()

print("Iniciando configuración de dispositivos...")
configurar(RUTA_CONSOLAR, R1_COMANDOS, 'R1') 
configurar(RUTA_CONSOLAS, SW1_COMANDOS, 'SW1')
print("Configuración de dispositivos finalizada.")
