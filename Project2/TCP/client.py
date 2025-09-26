#Ryan Tomas 028210102
#CECS 327
import socket, time
import random
random.seed()
servers = ["server1", "server2", "server3", "server4", "server5"]
host = random.choice(servers)
print(host)

TCP_port = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.connect((host, TCP_port))
    data = server.recv(1024)

print(f"Connected to {host}, got:", data.decode())
