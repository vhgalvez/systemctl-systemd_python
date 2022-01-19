import socket
import logging
import sys
import os


hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)

try:
    for port in range(1, 65535):
        s = socket. socket(socket .AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        resultado = s.connect_ex((ip, port))

        if resultado == 0:

            logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler("/tmp/port.log"),
                logging.StreamHandler(sys.stdout)
                ]
            )

            x = 1
            while (x >= 1):
                logging.debug('This message is skipped as a level is set as INFO')
                logging.info('So should this')
                logging.warning('And this, too')
                logging.error('Testing non-ASCII character, Ø and ö')
                logging.info('El puerto {} está abierto'. format(port) + os.linesep)

        s.close()

except:
    print("In Saliendo . .. ")
    sys.exit(0)
