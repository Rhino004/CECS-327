#Ryan Tomas 
#CECS 327 project 1 Docker
#step 2 run this command docker run hello-world
#step 3 docker run -ir alpine:latest sh
#step 4 run a python script that prints "hello Docker!"
print("Hello, Docker! This is my first containerized app.")
#in the terminal run docker build -t my-python-app .
#run container with docker run my-python-app
#pull nginx image :docker pull nginx:latest
#run the container with port mapping: docker run -d -p 8080:80 --name my-nginx nginx:latest