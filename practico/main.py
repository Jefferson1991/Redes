import netmiko as nm
from config import sw1, r1, comandos_r1, comandos_sw1

def configurar_dispositivo(dispositivo, comandos, nombre_dispositivo):
    try:
        conexion = nm.ConnectHandler(**dispositivo)
        conexion.enable()
        output = conexion.send_config_set(comandos)
        print(f"Configuración exitosa en {dispositivo['host']}:\n{output}")
        conexion.disconnect()
    except Exception as e:
        print(f"Error al configurar {dispositivo['host']}: {e}")    
        

if __name__ == "__main__":
    configurar_dispositivo(r1, comandos_r1)
    configurar_dispositivo(sw1, comandos_sw1) 
    print("Configuración de dispositivos completada.")
