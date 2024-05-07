# systemctl-systemd_python

Este repositorio contiene un script de Python que escanea los puertos de una dirección IP y registra la información en un archivo de registro. El script se puede ejecutar como un servicio de systemd en sistemas Linux.

Este script de Python es un escáner de puertos simple. Aquí está lo que hace, paso a paso:

1. **Obtención del nombre del host y la dirección IP**: Obtiene el nombre del host y la dirección IP de la máquina donde se ejecuta el script.

2. **Intento de conexión a cada puerto**: Intenta conectarse a cada puerto en el rango de 1 a 65535 en esa dirección IP.

3. **Configuración del registro si el puerto está abierto**: Si puede conectarse a un puerto (es decir, si `connect_ex` devuelve 0), configura un logger para registrar información.

4. **Manejadores del logger**: El logger tiene dos manejadores: uno que escribe en un archivo llamado "port.log" en el directorio "/tmp", y otro que escribe en la salida estándar.

5. **Bucle infinito de registro**: Luego, el script entra en un bucle infinito (ya que `x` siempre es mayor o igual a 1) donde registra varios mensajes. Los mensajes de nivel DEBUG e INFO no se mostrarán porque el nivel de registro se establece en INFO.

6. **Registro del puerto abierto**: También registra un mensaje que indica que el puerto está abierto.

7. **Cierre del socket**: Finalmente, cierra el socket.

8. **Manejo de excepciones**: Si ocurre alguna excepción durante este proceso, el script imprime "__Exit__" y termina.


https://towardsdev.com/create-service-systemctl-systemd-in-python-9a0e8b5ab6ae
