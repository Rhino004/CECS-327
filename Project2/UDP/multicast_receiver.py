import socket
import struct
import argparse
import time
import json
# Argument parsing
parser = argparse.ArgumentParser(description='Multicast UDP Receiver')
parser.add_argument('--duration', type=int, default=15, help='Duration to listen for messages (in seconds)')
args = parser.parse_args()

# Multicast group details
mcast_group = '224.1.1.1'
mcast_port = 5007
host_ip = socket.gethostbyname(socket.gethostname())
# Create the UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#listening on all interfaces

sock.bind(("", mcast_port))
# Join the multicast group

mreq = struct.pack("4s4s", socket.inet_aton(mcast_group), socket.inet_aton(host_ip))
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
print("[receiver]Listening on multicast group {}:{}".format(mcast_group, mcast_port))
# Set a timeout so the socket does not block indefinitely
sock.settimeout(0.5)
start = time.time()

# Listen for messages
while time.time() - start < args.duration:
    try:
        data, addr = sock.recvfrom(1024)
    except socket.timeout:
        continue  # just loop again until duration ends
    try:
        message = data.decode('utf-8')
        try:
            json_data = json.loads(message)
            print(f"[receiver] Received JSON from {addr}: {json_data}")
        except json.JSONDecodeError:
            print(f"[receiver] Received text from {addr}: {message}")
    except UnicodeDecodeError:
        print(f"[receiver] Received binary from {addr}: {data}")

# Leave the multicast group
sock.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreq)
sock.close()
print('[receiver] Leaving multicast group and closing socket.')