from netmiko import ConnectHandler

dispositivo = {
    'device_type': 'cisco_ios_telnet',
    'host': '127.0.0.1',
    'username': 'developer',
    'password': 'C1sco12345',
    'port': 2222,
    # Agregamos esto para darle un poco más de tiempo a la conexión Telnet
    'global_delay_factor': 2, 
}

print("Probando Netmiko vía Telnet al Router 1...")
try:
    conexion = ConnectHandler(**dispositivo)
    print("✅ Netmiko conectó exitosamente.")
    print(conexion.send_command("show ip int brief"))
    conexion.disconnect()
except Exception as e:
    print(f"❌ Error de Netmiko:\n{e}")