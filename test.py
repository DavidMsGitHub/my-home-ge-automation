import socket

# Get the hostname of the device
hostname = socket.gethostname()

# Get the IP address of the device
ip_address = socket.gethostbyname(hostname)

print(f"Hostname: {hostname}")
print(f"IP Address: {ip_address}")
