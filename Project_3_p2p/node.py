# Project_3_p2p/node.py
#To use flask we need to install it first using pip
#need flask to make a flask app, and jsonify to return json responses
#Also need request to handle incoming requests
from flask import Flask, jsonify, request
import  threading, time, uuid, requests, socket
import os
#giving each node a unique id
app = Flask(__name__)
node_id = str(uuid.uuid4())
peers = set()
#the bootstrap node url
#URL is from the docker network name
bootstrap_url = "http://bootstrap:5000"
node_url = os.environ.get("NODE_URL", f"http://{socket.gethostname()}:5000")

#route is the endpoint of the flask app
#this would be used on localhost:5000/
@app.route('/')
def index():
    return jsonify({"message": f"Node {node_id} is running!"})

#route to register a new peer
#POST is need for flask and is used to send data to the server
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    peer = data.get("peer")
    if peer:
        peers.add(peer)
        return jsonify({"status": "registered", "peers": list(peers)})
    #when the peer is missing in the request
    #400 is the status code for bad request
    return jsonify({"error": "peer missing"}), 400

#route to send a message to all peers
@app.route('/message', methods=['POST'])
def message():
    data = request.get_json()
    sender = data.get("sender")
    msg = data.get("msg")
    print(f"Received message from {sender}: {msg}")
    return jsonify({"status": "received"})

def register_with_bootstrap():
    try:
        res = requests.post(f"{bootstrap_url}/register", json={"peer": node_url})
        if res.status_code == 200:
            data = res.json()
            peers.update(data.get("peers", []))
            print(f"Registered with bootstrap. Known peers: {peers}")
    except Exception as e:
        print(f"Bootstrap registration failed: {e}")

def discover_peers():
    while True:
        for peer in list(peers):
            try:
                res = requests.get(f"{peer}/")
                if res.status_code == 200:
                    print(f"Contacted peer {peer}")
            except:
                peers.discard(peer)
        time.sleep(10)

#need the if statement to run the app only when this file is executed directly
if __name__ == '__main__':
    # Register with the bootstrap node
    #get the hostname of the machine
    app.config['HOSTNAME'] = socket.gethostname()
    #start a thread to register with bootstrap
    threading.Thread(target=register_with_bootstrap).start()
    threading.Thread(target=discover_peers, daemon=True).start()
    # Run the Flask application
    app.run(host='0.0.0.0', port=5000)