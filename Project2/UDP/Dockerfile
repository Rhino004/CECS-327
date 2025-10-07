FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /project2/UDP


COPY multicast_sender.py multicast_receiver.py ./
# Install tcpdump and iproute2
RUN apt-get update && apt-get install -y tcpdump iproute2 && rm -rf /var/lib/apt/lists/*

# Default command (can be overridden in docker-compose)
CMD ["python", "multicast_sender.py"]
