# CECS-327
# Project 2 A Bite of Distributed Communication
# Ryan Tomas 028210102

## Description
This project is to see the differences between TCP and UDP. This is done with anycast and multicast

** Commands to run on windows** 
# for anycast TCP folder
# for the server
- docker-compose up -d --build
- docker exec -it server1 tcpdump -i eth0 tcp port 5000 -n
# for the client 
- docker compose exec client python client.py
# multicast UDP folder
- docker compose up --build