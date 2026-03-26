# ============================================================
# consola_router.py — Acceso a router via consola serial del DevBox
# ============================================================
# ¿Por qué existe este archivo?
#   Router 2 no acepta SSH directo. Solo se puede acceder a su
#   consola serial desde el DevBox (un servidor Linux intermedio).
#   El flujo es: tu PC → SSH al DevBox → telnet a la consola del router
#
# Esta clase imita la interfaz de Netmiko (send_config_set, send_command,
# save_config, disconnect) para que el resto del código sea igual
# sin importar si el router usa SSH directo o consola.

import paramiko
import time


class ConsolaRouter:

    PROMPT_EXEC   = ['#']
    PROMPT_AUTH   = ['Username', 'username', 'Password', 'password', '#', '>']
    PROMPT_CONFIG = ['(config']

    def __init__(self, devbox_info, console_port, router_user, router_pass):
        # Paso 1: conectar al DevBox por SSH
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
        self._esperar_prompt(self.PROMPT_EXEC + ['$'], timeout=5)
        self._limpiar_buffer()

        # Paso 2: liberar el puerto si otra sesión lo tiene ocupado
        print(f"    [>] Liberando puerto {console_port} si hay sesión activa...")
        kill_cmd = (
            f"PID=$(ps aux | grep 'telnet localhost {console_port}' "
            f"| grep -v grep | awk '{{print $2}}') "
            f"&& [ -n \"$PID\" ] && kill $PID; sleep 1\n"
        )
        self.shell.send(kill_cmd)
        time.sleep(2)
        self._limpiar_buffer()

        # Paso 3: abrir la consola del router via telnet
        print(f"    [>] Abriendo consola del router (puerto {console_port})...")
        self.shell.send(f'telnet localhost {console_port}\n')
        time.sleep(4)
        self._limpiar_buffer()

        # Paso 4: despertar la consola y autenticarse
        self.shell.send('\n')
        salida = self._esperar_prompt(self.PROMPT_AUTH, timeout=15)

        if 'Username' in salida or 'username' in salida:
            self.shell.send(f'{router_user}\n')
            salida = self._esperar_prompt(['Password', 'password', '#', '>'], timeout=5)

        if 'Password' in salida or 'password' in salida:
            self.shell.send(f'{router_pass}\n')
            salida = self._esperar_prompt(['#', '>'], timeout=10)

        # Si quedó en modo usuario (>) pasar a enable
        if salida.rstrip().endswith('>'):
            self.shell.send('enable\n')
            salida = self._esperar_prompt(['Password', 'password', '#'], timeout=5)
            if 'Password' in salida or 'password' in salida:
                self.shell.send(f'{router_pass}\n')
                self._esperar_prompt(['#'], timeout=5)

        if '#' not in salida:
            self.shell.send('\n')
            self._esperar_prompt(['#'], timeout=5)

        self._limpiar_buffer()
        print(f"    [>] Sesión activa en el router.")

    # ----------------------------------------------------------
    # Métodos internos de lectura
    # ----------------------------------------------------------

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

    # ----------------------------------------------------------
    # Métodos públicos (misma interfaz que Netmiko)
    # ----------------------------------------------------------

    def send_config_set(self, commands):
        """Envía una lista de comandos en modo configuración."""
        self.shell.send('configure terminal\n')
        self._esperar_prompt(self.PROMPT_CONFIG, timeout=5)
        for cmd in commands:
            self.shell.send(f'{cmd}\n')
            time.sleep(0.5)
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
        salida = self._esperar_prompt(['[OK]', 'copy', '#'], timeout=10)
        if 'confirm' in salida.lower() or '[confirm]' in salida:
            self.shell.send('\n')
            self._esperar_prompt(['#'], timeout=10)
        return salida

    def disconnect(self):
        """Cierra la sesión telnet y la conexión SSH al DevBox."""
        try:
            self.shell.send('exit\n')
            time.sleep(0.5)
        except Exception:
            pass
        self.ssh.close()
