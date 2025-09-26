import socket
import os

host = "0.0.0.0"
port = 5000
#to get the container'server name 
server_name = os.getenv("SERVER_NAME", "default-server")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((host, port))
    server.listen()
    print(f"{server_name} ready on port {port}")

    while True:
        conn, addr = server.accept()
        with conn:
            print(f"{server_name} accepted connected by {addr}")
            message = f"Hello from {server_name}!"
            conn.sendall(message.encode())
            print("Sent: ", message)
