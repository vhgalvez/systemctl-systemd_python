from prometheus_client import start_http_server, Counter
import socket
import logging
import sys
import os

# Define un contador Prometheus para los puertos abiertos
PORT_OPEN_COUNTER = Counter('ports_opened', 'Number of ports opened')

def analyze_data(port, status):
    """Envía los datos del puerto escaneado a Prometheus"""
    if status == "open":
        PORT_OPEN_COUNTER.inc()  # Incrementa el contador de puertos abiertos

def scan_ports():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)

    try:
        for port in range(1, 65535):
            net = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            result = net.connect_ex((ip, port))

            if result == 0:
                logging.info('Port {} is open'.format(port))
                analyze_data(port, "open")
            else:
                analyze_data(port, "closed")

            net.close()

    except socket.error as e:
        logging.error('Socket error occurred: {}'.format(e))
    except Exception as e:
        logging.error('Error occurred: {}'.format(e))

if __name__ == "__main__":
    # Inicia un servidor HTTP para exponer métricas Prometheus
    start_http_server(8000)
    # Escanea los puertos
    scan_ports()
