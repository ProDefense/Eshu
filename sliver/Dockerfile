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

# Expose necessary ports for Sliver
EXPOSE 8888 31337

### Unpack Sliver:
RUN /opt/sliver-server unpack --force 

WORKDIR /home/sliver/
VOLUME [ "/home/sliver/.sliver" ]
ENTRYPOINT [ "/opt/sliver-server" ]
