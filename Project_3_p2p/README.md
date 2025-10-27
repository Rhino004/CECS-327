# CECS-327
# Project 3 peer to peer
# Ryan Tomas 028210102

## Description
This project is to make a peer 2 peer network with the use of Docker. The network would be able to function because of bootstrap and docker network. This allows communaction with docker containers which act as nodes.

** Commands to run on windows Bash**
# making a docker container for the nodes and bootstap
docker build -t p2p-node .
docker build -t bootstrap-node -f bootstrap.Dockerfile .
# need to create the network with 
docker network create p2p_network
# running bootstrap
docker run -d --name bootstrap --network p2p_network -p 5000:5000 bootstrap-node
# running 20 nodes
for i in {1..20}; do
PORT=$((5000 + i))
docker run -d --name node$i --network p2p_network \
    -p $PORT:5000 \
    -e NODE_PORT=$PORT \
    -e NODE_URL="http://node$i:5000" \
    -e BOOTSTRAP_URL="http://bootstrap:5000" \
    p2p-node
done

# sending messages at random
for i in {1..19}; do
SRC_PORT=$((5000 + (RANDOM % 20) + 1))
TARGET_PORT=$((5000 + (RANDOM % 20) + 1))
echo "sending from node$((SRC_PORT-5000)) to node$((TARGET_PORT-5000))"
curl -s -X POST "http://localhost:$TARGET_PORT/message" \
    -H "Content-Type: application/json" \
    -d "{\"sender\": \"node$((SRC_PORT-5000))\", \"msg\": \"Hello node$((TARGET_PORT-5000))\"}"
done
