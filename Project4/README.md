# CECS-327
# Project 4: Distribution and Scalability
# Ryan Tomas 028210102

## Description
This project builds upon our last project of peer-2-peer networking. I'm going have to add two features to the network. The feateures is to upload/download a file to the network and save it to a node. The network should  distribute the storage responsibility with the use of hashing.

**Commands to run on windows**
# compose the docker image
docker-compose up --build
# upload a file to the network whcih is node 1
curl -F 'file=@test.txt' http://localhost:5001/upload 
# download the file from the network
curl http://localhost:5001/download/test.txt -o download.txt

# storing values
curl -X POST http://localhost:5001/kv -H "Content-Type: 
application/json" -d '{"key": "color", "value": "blue"}' 

# #retrieving values

curl http://localhost:5001/kv/color