from netmiko import ConnectHandler
import paramiko
import time
import sys

# ============================================================
# SANDBOX: DevNet IOS XE Catalyst 8000v
# VPN AnyConnect requerido para acceder a 10.10.20.x
# ============================================================
#
# Switch Nexus 9K    → SSH directo      10.10.20.40:22  admin/RG!_Yw200
# Router 1 (Cat8k-1) → SSH directo      10.10.20.48:22  developer/C1sco12345
# Router 2 (Cat8k-2) → consola DevBox   10.10.20.50 → telnet localhost:2223
#
# NOTA: Los puertos 2222/2223 del DevBox solo son accesibles desde
# localhost del propio DevBox (no desde fuera via VPN). Por eso Router 2
# se accede via túnel SSH: tu máquina → DevBox (SSH) → router (telnet consola).

DEVBOX = {
    'host': '10.10.20.50',
    'username': 'developer',
    'password': 'C1sco12345',
}

# ============================================================
# CLASE: Acceso a router via consola serial del DevBox
# ============================================================

class ConsolaRouter:
    """
    Conecta a un router Cat8kv via la consola serial del DevBox.
    Flujo: SSH al DevBox → telnet localhost:<puerto_consola>
    Expone la misma interfaz que Netmiko para compatibilidad.
    """

    PROMPT_EXEC   = ['#']
    PROMPT_AUTH   = ['Username', 'username', 'Password', 'password', '#', '>']
    PROMPT_CONFIG = ['(config']

    def __init__(self, devbox_info, console_port, router_user, router_pass):
        print(f"    [>] SSH al DevBox ({devbox_info['host']})...")
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(
            hostname=devbox_info['host'],
            username=devbox_info['username'],
            password=devbox_info['password'],
            look_for_keys=False,
            allow_agent=False
        )
        self.shell = self.ssh.invoke_shell(width=200, height=50)
        self._esperar_prompt(self.PROMPT_EXEC + ['$'], timeout=5)  # prompt del DevBox
        self._limpiar_buffer()

        # Liberar el puerto si hay una sesión telnet ocupándolo (QEMU acepta solo una)
        print(f"    [>] Liberando puerto {console_port} si hay sesión activa...")
        kill_cmd = f"PID=$(ps aux | grep 'telnet localhost {console_port}' | grep -v grep | awk '{{print $2}}') && [ -n \"$PID\" ] && kill $PID; sleep 1\n"
        self.shell.send(kill_cmd)
        time.sleep(2)
        self._limpiar_buffer()

        print(f"    [>] Abriendo consola del router (puerto {console_port})...")
        self.shell.send(f'telnet localhost {console_port}\n')
        time.sleep(4)
        self._limpiar_buffer()

        # Enviar Enter para despertar la consola
        self.shell.send('\n')

        # Esperar prompt de autenticación o de router
        salida = self._esperar_prompt(self.PROMPT_AUTH, timeout=15)

        # Manejar autenticación si se solicita
        if 'Username' in salida or 'username' in salida:
            self.shell.send(f'{router_user}\n')
            salida = self._esperar_prompt(['Password', 'password', '#', '>'], timeout=5)

        if 'Password' in salida or 'password' in salida:
            self.shell.send(f'{router_pass}\n')
            salida = self._esperar_prompt(['#', '>'], timeout=10)

        # Si quedó en modo usuario (>), pasar a enable
        if salida.rstrip().endswith('>'):
            self.shell.send('enable\n')
            salida = self._esperar_prompt(['Password', 'password', '#'], timeout=5)
            if 'Password' in salida or 'password' in salida:
                self.shell.send(f'{router_pass}\n')
                self._esperar_prompt(['#'], timeout=5)

        # Enviar Enter extra en caso de que la consola esté inactiva
        if '#' not in salida:
            self.shell.send('\n')
            self._esperar_prompt(['#'], timeout=5)

        self._limpiar_buffer()
        print(f"    [>] Sesión activa en el router.")

    def _esperar(self, segundos):
        time.sleep(segundos)

    def _leer(self):
        """Lee todo lo disponible en el buffer."""
        salida = b''
        time.sleep(0.3)
        while self.shell.recv_ready():
            salida += self.shell.recv(65535)
            time.sleep(0.1)
        return salida.decode('utf-8', errors='ignore')

    def _esperar_prompt(self, prompts, timeout=15):
        """Lee hasta encontrar uno de los prompts o agotar el timeout."""
        salida = ''
        inicio = time.time()
        while time.time() - inicio < timeout:
            if self.shell.recv_ready():
                chunk = self.shell.recv(4096).decode('utf-8', errors='ignore')
                salida += chunk
                if any(p in salida for p in prompts):
                    break
            else:
                time.sleep(0.2)
        return salida

    def _limpiar_buffer(self):
        self._leer()

    def send_config_set(self, commands):
        """Envía lista de comandos en modo configuración."""
        self.shell.send('configure terminal\n')
        self._esperar_prompt(self.PROMPT_CONFIG, timeout=5)
        for cmd in commands:
            self.shell.send(f'{cmd}\n')
            self._esperar(0.5)
        self.shell.send('end\n')
        self._esperar_prompt(self.PROMPT_EXEC, timeout=5)
        return self._leer()

    def send_command(self, command, read_timeout=15):
        """Envía un comando EXEC y retorna la salida."""
        self.shell.send(f'{command}\n')
        self._esperar_prompt(self.PROMPT_EXEC, timeout=read_timeout)
        return self._leer()

    def save_config(self):
        """Guarda la configuración (write memory)."""
        self.shell.send('write memory\n')
        # Acepta confirmación automática si el IOS la pide
        salida = self._esperar_prompt(['[OK]', 'copy', '#'], timeout=10)
        if 'confirm' in salida.lower() or '[confirm]' in salida:
            self.shell.send('\n')
            self._esperar_prompt(['#'], timeout=10)
        return salida

    def disconnect(self):
        """Cierra la sesión y la conexión SSH al DevBox."""
        try:
            self.shell.send('exit\n')
            self._esperar(0.5)
        except Exception:
            pass
        self.ssh.close()


# ============================================================
# DICCIONARIOS DE DISPOSITIVOS
# ============================================================

devices = {
    'switch_nexus': {
        'tipo': 'netmiko',
        'params': {
            'device_type': 'cisco_nxos',
            'host': '10.10.20.40',
            'username': 'admin',
            'password': 'RG!_Yw200',
            'global_delay_factor': 2,
        }
    },
    'router1': {
        'tipo': 'netmiko',
        'params': {
            'device_type': 'cisco_ios',
            'host': '10.10.20.48',          # Cat8k-1 — SSH directo confirmado
            'username': 'developer',
            'password': 'C1sco12345',
            'global_delay_factor': 2,
        }
    },
    'router2': {
        'tipo': 'consola',                  # Cat8k-2 — via consola DevBox
        'console_port': 2223,
        'router_user': 'developer',
        'router_pass': 'C1sco12345',
    }
}

# ============================================================
# COMANDOS DE CONFIGURACIÓN
# ============================================================

config_commands = {
    'switch_nexus': [
        'banner motd #ADVERTENCIA: Acceso autorizado únicamente a personal de TI#',
        'vlan 10',
        'name VLAN_COMPARTIDA',
        'exit',
        # IMPORTANTE: Verificar interfaces con 'show cdp neighbors' si es necesario
        'interface Ethernet1/1',
        'switchport',
        'switchport mode trunk',
        'switchport trunk allowed vlan 10',
        'no shutdown',
        'interface Ethernet1/2',
        'switchport',
        'switchport mode trunk',
        'switchport trunk allowed vlan 10',
        'no shutdown',
    ],
    'router1': [
        'banner motd #ADVERTENCIA: Acceso autorizado únicamente a personal de TI#',
        'service password-encryption',
        'no ip domain-lookup',
        'ip ssh version 2',
        'ip ssh authentication-retries 3',
        'ip ssh time-out 60',
        'line vty 0 4',
        'exec-timeout 5 0',
        'transport input ssh',
        'exit',
        'interface GigabitEthernet2',
        'no shutdown',
        'interface GigabitEthernet2.10',
        'encapsulation dot1Q 10',
        'ip address 192.168.10.1 255.255.255.0',
        'no shutdown',
    ],
    'router2': [
        # cat8k-pod02 solo tiene GigabitEthernet1 (una sola NIC en QEMU)
        'service password-encryption',
        'no ip domain-lookup',
        'interface GigabitEthernet1',
        'no shutdown',
        'interface GigabitEthernet1.10',
        'encapsulation dot1Q 10',
        'ip address 192.168.10.2 255.255.255.0',
        'no shutdown',
    ],
}

# ============================================================
# FUNCIONES
# ============================================================

def conectar(device_name):
    """Establece conexión con el dispositivo según su tipo."""
    dev = devices[device_name]

    if dev['tipo'] == 'netmiko':
        host = dev['params']['host']
        print(f"\n[*] Conectando a {host} ({device_name}) via SSH...")
        try:
            conexion = ConnectHandler(**dev['params'])
            print(f"[+] Conexión establecida con {device_name}.")
            return conexion
        except Exception as e:
            print(f"[-] Error conectando a {device_name}: {e}")
            return None

    else:  # consola via DevBox
        print(f"\n[*] Conectando a {device_name} via consola del DevBox...")
        try:
            conexion = ConsolaRouter(
                DEVBOX,
                dev['console_port'],
                dev['router_user'],
                dev['router_pass']
            )
            print(f"[+] Conexión establecida con {device_name}.")
            return conexion
        except Exception as e:
            print(f"[-] Error conectando a {device_name}: {e}")
            return None


def enviar_comandos(conexion, device_name):
    """Envía comandos de configuración y guarda la configuración."""
    print(f"[*] Enviando comandos a {device_name}...")
    try:
        conexion.send_config_set(config_commands[device_name])
        conexion.save_config()
        print(f"[+] Configuración aplicada y guardada en {device_name}.")
    except Exception as e:
        print(f"[-] Error enviando comandos a {device_name}: {e}")


# ============================================================
# MENÚ PRINCIPAL
# ============================================================

def main():
    print("=== Automatización de Infraestructura de Red ===")
    print("REQUISITO: VPN AnyConnect del sandbox debe estar activa.\n")
    print("¿Qué desea configurar?")
    print("  1. Solo Switch Nexus 9K")
    print("  2. Solo Routers (R1 y R2)")
    print("  3. Todo (Switch + Routers + Validación de ping)")

    choice = input("\nSeleccione opción (1-3): ")

    if choice == '1':
        device_list = ['switch_nexus']
    elif choice == '2':
        device_list = ['router1', 'router2']
    elif choice == '3':
        device_list = ['switch_nexus', 'router1', 'router2']
    else:
        print("[-] Opción inválida. Saliendo...")
        sys.exit(1)

    conexiones = {}
    for device_name in device_list:
        conexion = conectar(device_name)
        if conexion:
            enviar_comandos(conexion, device_name)
            conexiones[device_name] = conexion
        else:
            print(f"[-] No se pudo configurar {device_name}.")

    # Validación con ping (solo opción 3 con ambos routers activos)
    if choice == '3' and 'router2' in conexiones:
        print("\n[*] Esperando 5 segundos para convergencia de red...")
        time.sleep(5)
        print("Enviando ping desde Router 2 (192.168.10.2) hacia Router 1 (192.168.10.1)...")
        resultado_ping = conexiones['router2'].send_command(
            "ping 192.168.10.1 source GigabitEthernet1.10", read_timeout=15
        )
        print("\n--- Resultado Final del Ping ---")
        print(resultado_ping)
        print("--------------------------------")

    for device_name, conexion in conexiones.items():
        conexion.disconnect()
        print(f"[*] Conexión cerrada: {device_name}")

    print("\n¡Despliegue finalizado exitosamente!")


if __name__ == '__main__':
    main()
