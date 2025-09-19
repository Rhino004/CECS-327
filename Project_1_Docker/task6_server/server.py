import time
import socket
import threading

host = '0.0.0.0'
TCP_port = 5000
#connects the TCP clients in its own thread
def handle_tcp(connection,addr):
    print(f"TCP Connected by the address {addr}")
    with connection: #checks if there is a connection
        connection.sendall(b"This is the TCP server in the Docker container")
        while True:
            data = connection.recv(1024)#1024 is the bytes
            if not data: #close the connection if there is not 
                break
            print(f"TCP Received from  address {addr}: {data.decode()}")
            connection.sendall(data)#echo message to the client

def tcp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, TCP_port)) #
        server.listen()
        print(f"TCP Listening on the host and port: {host}:{TCP_port}")
        while True:
            connection, addr = server.accept()#accetps new client
            #threading is used to give access to multiple clients at the same time
            threading.Thread(target=handle_tcp, args=(connection, addr)).start()



threading.Thread(target=tcp_server, daemon=True).start()#runs the function in parallel for multiple clients
print("Server is running")
try:
    while True:#this checks if the server is runningS
        time.sleep(2)
except KeyboardInterrupt:#when it ends
    print("Server shutting down.")
#to do this task I want to do this command
#docker-compose up --build