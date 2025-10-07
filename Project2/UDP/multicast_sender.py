import socket
import struct
import json
import os
import random

mcast_group = '224.1.1.1'
mcast_port = 5007

sensor_name = os.getenv('SENSOR_NAME', 'Sensor1')

# Create the UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
ttl = struct.pack('b', 1)  # Set TTL to 1
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

#plain text
messages = ["Hello, this is a multicast message."]
sock.sendto(messages[0].encode('utf-8'), (mcast_group, mcast_port))
print(f"[sender] Sent plain text message: {messages[0]}")

# JSON data
json_msg = json.dumps({"sensor": sensor_name, "value": round(20 + 5* random.random(), 2)})
sock.sendto(json_msg.encode('utf-8'), (mcast_group, mcast_port))
print(f"[sender] Sent JSON message: {json_msg}")

# Binary data
binary_data = os.urandom(16)  # 16 bytes of random binary data
sock.sendto(binary_data, (mcast_group, mcast_port))
print(f"[sender] Sent binary data: {binary_data}")