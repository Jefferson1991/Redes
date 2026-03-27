# Checklist pre-examen (ultra corto)

## 1) Elegir script correcto
- [ ] Si el entorno es CML con Console Server: usar `Router-on-a-Stick/` o `Router-dhcp/`.
- [ ] Si el entorno es local/directo: usar `Router-on-a-Stick-default/`.

## 2) Validar `config.py` antes de ejecutar
- [ ] `host` o rutas de consola correctas para el lab actual.
- [ ] `username`, `password`, `secret` correctos.
- [ ] `device_type` correcto (`cisco_ios` o `cisco_ios_telnet`).

## 3) Conectividad mínima
- [ ] VPN activa (si aplica).
- [ ] Ping a IP de gestión (si es conexión directa).
- [ ] Nodo/router/switch en estado `BOOTED` en CML.

## 4) Ejecución recomendada
- [ ] Ejecutar primero Router (`1`).
- [ ] Ejecutar luego Switch (`2`).
- [ ] No aplicar DHCP y estático mezclados en el mismo lab sin limpiar.

## 5) Comprobación técnica rápida
- [ ] Router: `show ip interface brief`
- [ ] Switch: `show interfaces status`
- [ ] Trunk: `show interfaces trunk`
- [ ] VLAN: `show vlan brief`

## 6) Si usas DHCP
- [ ] Router: `show ip dhcp pool`
- [ ] Router: `show ip dhcp binding`
- [ ] Host Linux: `dhclient -v eth0` y `ip addr show eth0`

## 7) Si algo falla
- [ ] Revisar interfaz física correcta en la topología.
- [ ] Revisar puerto trunk vs puerto access.
- [ ] Revisar gateway y máscara por VLAN.
- [ ] Volver a ejecutar por bloques (R1 primero, SW1 después).

## 8) Cierre
- [ ] `write memory` en equipos.
- [ ] Guardar evidencia (capturas de comandos clave).
- [ ] Confirmar que el script corresponde al escenario del examen.
