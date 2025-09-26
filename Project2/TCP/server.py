import socket
import os

host = "0.0.0.0"
PORT = 5000

server_name = os.getenv("SERVER_NAME", "default-server")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, PORT))
    s.listen()

    print(f"{server_name} listening on port {PORT}")

    while True:
        conn, addr = s.accept()
        with conn:
            print(f"{server_name} connected by {addr}")
            message = f"Hello from {server_name}!"
            conn.sendall(message.encode())
