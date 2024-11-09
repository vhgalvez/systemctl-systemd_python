# systemctl-systemd_python

This repository contains a Python script that scans the ports of an IP address and logs the information to a log file. The script can be run as a systemd service on Linux systems.

## Script Description

This Python script is a simple port scanner. Here is what it does, step by step:

1. **Getting the hostname and IP address**: It obtains the hostname and IP address of the machine where the script is running.

2. **Attempt to connect to each port**: It tries to connect to each port in the range from 1 to 65535 on that IP address.

3. **Logging configuration if the port is open**: If it can connect to a port (i.e., if `connect_ex` returns 0), it sets up a logger to record information.

4. **Logger handlers**: The logger has two handlers: one that writes to a file named "port.log" in the "/tmp" directory, and another that writes to standard output.

5. **Infinite logging loop**: The script then enters an infinite loop where it logs various messages. DEBUG and INFO level messages will not be shown because the logging level is set to INFO.

6. **Logging the open port**: It logs a message indicating that the port is open.

7. **Closing the socket**: Finally, it closes the socket.

8. **Exception handling**: If any exception occurs during this process, the script prints "Exit" and terminates.

## Running as a systemd Service

The script is designed to be run as a systemd service on Linux systems, making it easy to automatically run the scanner when the system starts. You can create a systemd unit file to manage the script as a service.

For more information on how to create a service with systemctl/systemd, you can refer to the following link: [Create Service systemctl-systemd in Python](https://towardsdev.com/create-service-systemctl-systemd-in-python-9a0e8b5ab6ae).

## Requirements

- Python 3
- Administrator permissions to register the script as a systemd service

## Installation and Configuration
1. Clone this repository:
   ```bash
   git clone <REPOSITORY_URL>
   ```
2. Navigate to the repository directory:
   ```bash
   cd systemctl-systemd_python
   ```
3. Make sure you have Python 3 installed on your system.
4. Create the systemd unit file at `/etc/systemd/system/port-scanner.service` with the following content:
   ```ini
   [Unit]
   Description=Port Scanner Service
   After=network.target

   [Service]
   ExecStart=/usr/bin/python3 /path/to/script.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```
5. Reload the systemd services:
   ```bash
   sudo systemctl daemon-reload
   ```
6. Enable the service to start automatically on system boot:
   ```bash
   sudo systemctl enable port-scanner.service
   ```
7. Start the service:
   ```bash
   sudo systemctl start port-scanner.service
   ```

## Usage

The script will start scanning the ports of the host IP address and log the information to the `/tmp/port.log` file. You can check the status of the service using:
```bash
sudo systemctl status port-scanner.service
```


## Contribution
If you want to contribute to this project, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License. Please see the `LICENSE` file for more details.


https://towardsdev.com/create-service-systemctl-systemd-in-python-9a0e8b5ab6ae

