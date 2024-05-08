# Adapted from OpenAI's Vision example
from openai import OpenAI
import base64
import requests
from prometheus_client import start_http_server, Counter
import socket
import logging
import sys
import os

# Setup basic logging
logging.basicConfig(level=logging.INFO, filename="/tmp/script_log.log", filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Define a Prometheus counter for the number of open ports
PORT_OPEN_COUNTER = Counter('ports_opened', 'Number of ports opened')

# Configure the OpenAI client for local API use
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")


def analyze_port_with_gpt4(port, status):
    """Send port status to GPT-4 for analysis and log the response."""
    try:
        # Prepare the payload for the API call
        gpt4_payload = {
            "model": "davinci",
            "prompt": f"Analyze the security implications of a port being {'open' if status == 0 else 'closed'} on port {port}.",
            "max_tokens": 150
        }
        response = requests.post(f"{client.base_url}/engines/davinci/completions",
                                 json=gpt4_payload, headers={"Authorization": f"Bearer {client.api_key}"})
        response.raise_for_status()  # Ensures HTTP request errors are checked
        data = response.json()['choices'][0]['text']
        logging.info(f"GPT-4 analysis for port {port}: {data}")
        return data
    except Exception as e:
        logging.error(f"Error while analyzing port {port} with GPT-4: {e}")
        return None


def scan_ports():
    """Scan all ports on the local machine, log their status, and analyze open ports using GPT-4."""
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    logging.info(f"Starting port scan on {ip}")

    for port in range(1, 65535):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as net:
            net.settimeout(1)
            result = net.connect_ex((ip, port))
            if result == 0:
                PORT_OPEN_COUNTER.inc()
                logging.info(f'Port {port} is open')
                analysis = analyze_port_with_gpt4(port, result)
                logging.info(f'Analysis for port {port}: {analysis}')
            else:
                logging.info(f'Port {port} is closed')


if __name__ == "__main__":
    # Start a Prometheus HTTP server to expose metrics
    start_http_server(8000)
    # Scan ports
    scan_ports()