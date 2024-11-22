# Base image: Using an Ubuntu image to install dependencies
FROM ubuntu:22.04

# Set environment variables for non-interactive installation
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary packages
RUN apt-get update && apt-get install -y \
    software-properties-common \
    wget \
    sudo \
    curl \
    git \
    golang \
    build-essential \
    unzip \
    && add-apt-repository universe \
    && add-apt-repository multiverse \
    && apt-get update \
    && apt-get install -y \
    mingw-w64 \
    binutils-mingw-w64 \
    g++-mingw-w64 \
    && rm -rf /var/lib/apt/lists/*

# Manually download and install Sliver, skipping systemd configuration
RUN wget https://github.com/BishopFox/sliver/releases/latest/download/sliver-server_linux \
    && chmod +x sliver-server_linux \
    && mv sliver-server_linux /usr/local/bin/sliver-server \
    && wget https://github.com/BishopFox/sliver/releases/latest/download/sliver-client_linux \
    && chmod +x sliver-client_linux \
    && mv sliver-client_linux /usr/local/bin/sliver-client

# Expose necessary ports for Sliver
EXPOSE 8888 31337

# Set the working directory to the Sliver binary location
WORKDIR /opt/sliver/

# Volume to persist Sliver data
VOLUME [ "/opt/sliver/.sliver" ]

# Start Sliver server directly as the container's main process
CMD ["/usr/local/bin/sliver-server"]
