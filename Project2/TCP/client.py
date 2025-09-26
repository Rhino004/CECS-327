#Ryan Tomas 028210102
#CECS 327
import socket, time
import random
#need to seed random to change the outcome
random.seed()
servers = ["server1", "server2", "server3", "server4", "server5"]
host = random.choice(servers)
#a radom server is picked
print(host)

port = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.connect((host, port))
    data = server.recv(1024)

print(f"Received: ", data.decode())
