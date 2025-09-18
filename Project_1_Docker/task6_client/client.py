import socket, time

host = "server"  
TCP_port = 5000

def tcp_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.connect((host, TCP_port)) #connect with the server
        server.sendall(b"Hello from TCP client") #send a message to TCP server
        data = server.recv(1024)
        print(f"TCP Client Received: {data.decode()}") #The client would decode the data from the server

time.sleep(3) 
tcp_client()

