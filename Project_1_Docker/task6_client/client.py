#Ryan Tomas 028210102
#CECS 327
import socket, time

host = "server"  
TCP_port = 5000

time.sleep(3) 
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((host, TCP_port)) #connect with the client
        client.sendall(b"Hello from TCP client that is using Docker in the server ") #send a message to TCP server
        data = client.recv(1024)
        print(f"TCP Client Received from the TCP server: {data.decode()} ") #The client would decode the data from the server
        if not data:
                print("Server close connection")
        time.sleep(2)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((host, TCP_port)) #connect with the client
        client.sendall(b"Hello from TCP client that is using Docker") #send a message to TCP server
        data = client.recv(1024)
        print(f"TCP Client Received from the TCP client: {data.decode()}") #The client would decode the data from the server
        data = client.recv(1024)
        if not data:
                print("Server close connection")

        time.sleep(5)


