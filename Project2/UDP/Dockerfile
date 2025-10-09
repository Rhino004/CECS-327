FROM python:3.11-slim

WORKDIR /project2/UDP
COPY multicast_sender.py multicast_receiver.py ./

# Install tcpdump for monitoring
RUN apt-get update && \
    apt-get install -y tcpdump iproute2 iputils-ping && \
    rm -rf /var/lib/apt/lists/*

# Default command: run tcpdump for 15s in background, then run receiver for 15s
CMD sh -c "timeout 15 tcpdump -i eth0 udp port 5007 -n -l & python multicast_receiver.py --duration 15"


