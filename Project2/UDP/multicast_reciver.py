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

# Create the UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#listening on all interfaces

sock.bind(("", mcast_port))
# Join the multicast group

mreq = struct.pack("4sl", socket.inet_aton(mcast_group), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
print("Listening on multicast group {}:{}".format(mcast_group, mcast_port))
# Set a timeout so the socket does not block indefinitely

start = time.time()
last_time = start

# Listen for messages
while time.time() - start < args.duration:
    data, addr = sock.recvfrom(1024)
    now = time.time()
    print("[receiver] Time since last message: {:.6f} seconds".format(now - last_time))
    
    try:
        message = data.decode('utf-8')

        try:
            json_data = json.loads(message)
            print(f"[receiver] Received JSON data from {addr}: {json_data}")

        except json.JSONDecodeError:
            print(f"[receiver] Received non-JSON message from {addr}: {message}")

    except UnicodeDecodeError:
        print(f"[receiver] Received binary data from {addr}: {message}")

    last_time = now
    print("[receiver] Time taken to receive message: {:.6f} seconds".format(last_time - start))

# Leave the multicast group
sock.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreq)
sock.close()
print('[receiver] Leaving multicast group and closing socket.')