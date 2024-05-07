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


def process_image(path):
    """Process an image file from a given path and analyze it using the OpenAI API."""
    try:
        # Read the image and encode it to base64
        with open(path.replace("'", ""), "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as e:
        logging.error(f"Couldn't read the image at {path}: {e}")
        return

    # Generate a completion with the image
    try:
        completion = client.chat.completions.create(
            model="davinci",  # Ensure the model identifier is correct
            messages=[
                {
                    "role": "system",
                    "content": "This is a chat between a user and an assistant. The assistant is helping the user to describe an image."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What’s in this image?"},
                        {"type": "image_url", "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]
                }
            ],
            max_tokens=1000,
            stream=False
        )
        for message in completion['choices'][0]['messages']:
            if message['role'] == 'assistant':
                print(message['content'])
    except Exception as e:
        logging.error(f"Error during API completion: {e}")


def analyze_data(port, status):
    """Send scanned port data to Prometheus and a local GPT-4 API."""
    if status == "open":
        PORT_OPEN_COUNTER.inc()  # Increment the Prometheus counter for open ports

    try:
        # Send data to the GPT-4 API for analysis
        gpt4_api_url = "http://localhost:1234/v1/engines/davinci/completions"
        gpt4_payload = {
            "model": "davinci",
            "messages": [
                {
                    "role": "system",
                    "content": "Analyzing network port data."
                },
                {
                    "role": "user",
                    "content": f"Port number: {port}, Status: {status}"
                }
            ],
            "max_tokens": 100
        }
        response = requests.post(gpt4_api_url, json=gpt4_payload)
        response.raise_for_status()  # Check for HTTP request errors
        data = response.json()
        logging.info(f"Response from GPT-4 for port {port}: {data}")
    except Exception as e:
        logging.error(f"Error while analyzing data for port {port}: {e}")


def scan_ports():
    """Scan all ports on the local machine and log their status."""
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    logging.info(f"Starting port scan on {ip}")

    for port in range(1, 65535):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as net:
            net.settimeout(1)
            result = net.connect_ex((ip, port))
            if result == 0:
                logging.info(f'Port {port} is open')
                analyze_data(port, "open")
            else:
                analyze_data(port, "closed")


if __name__ == "__main__":
    # Ask the user for a path on the filesystem
    image_path = input("Enter a local filepath to an image: ")
    process_image(image_path)

    # Start a Prometheus HTTP server to expose metrics
    start_http_server(8000)
    # Scan ports
    scan_ports()
