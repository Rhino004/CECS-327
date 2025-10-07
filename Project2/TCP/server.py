import socket
import os

host = "0.0.0.0"
port = 5000
#to get the container'server name 
server_name = os.getenv("server_name", "default-server")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((host, port))#bind to all interfaces
    server.listen()#start listening for connections
    #print a message when the server is ready
    print(f"{server_name} ready on port {port}")
    #accept connections in a loop

    while True:
        conn, addr = server.accept()
        with conn:
            #print a message when a client connects
            print(f"[server] {server_name} accepted connection from {addr}")
            #send a message to the client
            message = f"Hello from {server_name}!"
            conn.sendall(message.encode())
            print("[server] Sent: ", message)
