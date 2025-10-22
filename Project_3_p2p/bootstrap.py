from flask import Flask, jsonify, request
# Initialize the Flask application
app = Flask(__name__)
peers = set()

#we need the @ symbol for decorators in python
#Decorator to define a route for registering peers
#register_peer function to handle peer registration
#POST method is used to send data to the server
@app.route('/register', methods=['POST'])
def register_peer():
    # Get the peer address from the request
    data = request.get_json()
    peer_address = data.get('address')
    if peer_address:
        peers.add(peer_address)
        # Return a success response
        #201 is the status code for created
        return jsonify({'message': 'Peer registered successfully.'}), 201
    
    #when the peer is missing in the request
    #400 is the status code for bad request
    return jsonify({'error': 'No address provided.'}), 400

#peer retrieval route
@app.route('/peers', methods=['GET'])
def get_peers():
    # Return the list of registered peers
    #200 is the status code for OK
    return jsonify(list(peers)), 200

if __name__ == '__main__':
    # Run the Flask application
    app.run(host='0.0.0.0', port=5000)