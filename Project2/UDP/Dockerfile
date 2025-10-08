FROM python:3.11-slim

WORKDIR /project2/UDP
COPY multicast_sender.py multicast_receiver.py ./

# Install tcpdump for monitoring and ping for network tests
RUN apt-get update && \
    apt-get install -y tcpdump iproute2 iputils-ping && \
    rm -rf /var/lib/apt/lists/*

# Default command for container
CMD ["python", "multicast_receiver.py", "--duration", "15"]
