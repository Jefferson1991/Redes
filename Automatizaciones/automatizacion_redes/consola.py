import paramiko
import time

class ConsolaRouter:
    """Accede a un router via consola serial del DevBox: SSH → telnet."""

    def __init__(self, devbox, puerto, usuario, clave):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(devbox['host'], username=devbox['username'],
                         password=devbox['password'], look_for_keys=False)
        self.shell = self.ssh.invoke_shell(width=200, height=50)
        self._esperar(['#', '$'])

        # Liberar puerto si está ocupado
        self.shell.send(f"kill $(ps aux | grep 'telnet localhost {puerto}' | grep -v grep | awk '{{print $2}}') 2>/dev/null; sleep 1\n")
        time.sleep(2)
        self._leer()

        # Abrir consola del router
        self.shell.send(f'telnet localhost {puerto}\n')
        time.sleep(4)
        self.shell.send('\n')
        salida = self._esperar(['Username', 'username', 'Password', 'password', '#', '>'])

        if 'sername' in salida:
            self.shell.send(f'{usuario}\n')
            salida = self._esperar(['Password', 'password', '#', '>'])
        if 'assword' in salida:
            self.shell.send(f'{clave}\n')
            salida = self._esperar(['#', '>'])
        if salida.rstrip().endswith('>'):
            self.shell.send('enable\n')
            self._esperar(['#'])

        self._leer()

    def _leer(self):
        salida = b''
        time.sleep(0.3)
        while self.shell.recv_ready():
            salida += self.shell.recv(65535)
            time.sleep(0.1)
        return salida.decode('utf-8', errors='ignore')

    def _esperar(self, prompts, timeout=15):
        salida = ''
        fin = time.time() + timeout
        while time.time() < fin:
            if self.shell.recv_ready():
                salida += self.shell.recv(4096).decode('utf-8', errors='ignore')
                if any(p in salida for p in prompts):
                    break
            else:
                time.sleep(0.2)
        return salida

    def send_config_set(self, commands):
        self.shell.send('configure terminal\n')
        self._esperar(['(config'])
        for cmd in commands:
            self.shell.send(f'{cmd}\n')
            time.sleep(0.5)
        self.shell.send('end\n')
        self._esperar(['#'])
        return self._leer()

    def send_command(self, command, read_timeout=15):
        self.shell.send(f'{command}\n')
        self._esperar(['#'], timeout=read_timeout)
        return self._leer()

    def save_config(self):
        self.shell.send('write memory\n')
        salida = self._esperar(['[OK]', '#'], timeout=10)
        if 'confirm' in salida.lower():
            self.shell.send('\n')
            self._esperar(['#'])

    def disconnect(self):
        try:
            self.shell.send('exit\n')
            time.sleep(0.5)
        except Exception:
            pass
        self.ssh.close()
