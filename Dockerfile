# Start with the Ubuntu 22.04 base image
FROM ubuntu:22.04

# Set the non-interactive mode for apt
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and install necessary packages
RUN apt-get update && apt-get install -y \
    python3 python3-pip vim nano curl wget bash nmap netcat \
    hydra ruby ruby-dev build-essential iproute2 net-tools \
    openssl libreadline-dev zlib1g-dev libpcap-dev git \
    lsb-release software-properties-common \
    iputils-ping iputils-tracepath iputils-arping dnsutils \
    openssh-server ruby-full libssl-dev \
    libsqlite3-dev libpq-dev libyaml-dev \
    libxml2-dev libxslt1-dev \
    mingw-w64 binutils-mingw-w64 g++-mingw-w64 mingw-w64-tools gcc-mingw-w64 \
    libcurl4-openssl-dev libgmp-dev sudo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set Python3 as the default Python command
RUN ln -sf python3 /usr/bin/python

# Set the default shell to Bash
SHELL ["/bin/bash", "-c"]

# Install Python packages
RUN pip install --upgrade pip setuptools
RUN pip install pymetasploit3 sliver-py

# Install Metasploit
RUN git clone https://github.com/rapid7/metasploit-framework.git /opt/metasploit-framework && \
    cd /opt/metasploit-framework && \
    git submodule init && \
    git submodule update && \
    gem install bundler && \
    bundle install

# Add Metasploit to PATH
ENV PATH="/opt/metasploit-framework/:$PATH"

# Copy the Metasploit RC file
COPY ./src/config_files/msfconsole.rc /opt/metasploit-framework/msfconsole.rc

# Install Sliver Client and Server
RUN wget https://github.com/BishopFox/sliver/releases/download/v1.5.42/sliver-client_linux && \
    wget https://github.com/BishopFox/sliver/releases/download/v1.5.42/sliver-server_linux && \
    chmod +x sliver-client_linux sliver-server_linux && \
    mv sliver-client_linux /usr/local/bin/sliver-client && \
    mv sliver-server_linux /usr/local/bin/sliver-server

# Set up the workspace for the Eshu library
WORKDIR /workspace/eshuCLP
COPY ./src/ /workspace/eshuCLP/

# Install the Eshu Python package
RUN pip install .

# Set the working directory for runtime
WORKDIR /workspace

# Expose necessary ports for Metasploit and other services
EXPOSE 80 4444 8080 55552 55553

# Run the msfconsole and keep the container running
CMD ["bash"]
