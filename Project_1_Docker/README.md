# CECS-327
# project 1 Docker
# Ryan Tomas 028210102

## Description
This project is to get familiar with Docker and to deploy a server and multi-container 

** Commands to run on windows** 
# multi-Container
- docker-compose up --build
# deploy a web server with local HTML
- docker run -d -p 8080:80 -v ${PWD}/index.html:/usr/share/nginx/html/index.html nginx:latest