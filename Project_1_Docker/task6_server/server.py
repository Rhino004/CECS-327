import time
import socket
import threading

host = '0.0.0.0'
TCP_port = 5000
UDP_port = 5001
#connects the TCP clients in its own thread
def handle_tcp(conn,addr):
    print(f"TCP Connected by the address {addr}")
    with conn: #checks if there is a connection
        while True:
            data = conn.recv(1024)#1024 is the bytes
            if not data: #close the connection if there is not 
                break
            print(f"TCP Received from  address {addr}: {data.decode()}")
            conn.sendall(data)#echo message to the client

def tcp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, TCP_port)) #
        server.listen()
        print(f"TCP Listening on the host and port: {host}:{TCP_port}")
        while True:
            conn, addr = server.accept()#accetps new client
            #threading is used to give access to multiple clients at the same time
            threading.Thread(target=handle_tcp, args=(conn, addr)).start()



threading.Thread(target=tcp_server, daemon=True).start()#runs the function in parallel for multiple clients
print("Server is running")
try:
    while True:#this checks if the server is runningS
        time.sleep(1)
except KeyboardInterrupt:#when it ends
    print("Server shutting down.")
#to do this task I want to do this command
#docker-compose up --build