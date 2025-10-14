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

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        print(f'[client] Connecting to {host} on port {port}')
        server.connect((host, port))
        data = server.recv(1024)
    
except Exception as e:
    print(f"[client] Connection to {host} failed, retrying...")
    time.sleep(1)
print(f"[client] Received: ", data.decode())
print("[client] Client done")

#docker exec -it server1 tcpdump -i eth0 udp port 5000 -n
#docker compose exec client python client.py