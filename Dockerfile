# Start with the Ubuntu 22.04 base image
FROM ubuntu:22.04

# Set the non-interactive mode for apt
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and install necessary packages
RUN apt-get update && apt-get install -y \
    python3 python3-pip vim nano curl wget bash nmap netcat \
    hydra ruby ruby-dev build-essential iproute2 net-tools\
    openssl libreadline-dev zlib1g-dev libpcap-dev git \
    lsb-release software-properties-common \
    iputils-ping iputils-tracepath iputils-arping dnsutils \
    openssh-server ruby-full libssl-dev \
    libsqlite3-dev libpq-dev libyaml-dev \
    libxml2-dev libxslt1-dev \
    mingw-w64 binutils-mingw-w64 g++-mingw-w64 mingw-w64-tools gcc-mingw-w64 \ 
    libcurl4-openssl-dev libgmp-dev sudo libffi-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set Python3 as the default Python command
RUN ln -sf python3 /usr/bin/python

# Set the default shell to Bash
SHELL ["/bin/bash", "-c"]

# Install pymetasploit3
RUN pip install pymetasploit3

# Install Metasploit
RUN git clone https://github.com/rapid7/metasploit-framework.git /opt/metasploit-framework && \
    cd /opt/metasploit-framework && \
    git submodule init && \
    git submodule update && \
    gem install bundler && \
    bundle install

ENV PATH="/opt/metasploit-framework/:$PATH"

# Run the msfconsole.rc commands and start Metasploit RPC service
COPY ./src/config_files/msfconsole.rc /opt/metasploit-framework/msfconsole.rc

# Install Sliver-py
RUN pip install sliver-py

# Sliver Client and Sliver Server

RUN wget https://github.com/BishopFox/sliver/releases/download/v1.5.42/sliver-client_linux

RUN wget https://github.com/BishopFox/sliver/releases/download/v1.5.42/sliver-server_linux

RUN chmod +x sliver-client_linux sliver-server_linux && \
    mv sliver-client_linux /usr/local/bin/sliver-client && \
    mv sliver-server_linux /usr/local/bin/sliver-server

# Commenting out this line because its un necessary if we are overriding the rc file anyway
# Also environment args in dockercompose do not apply here, you will need to set build args for that to pass correctl.y
#RUN echo "load msgrpc Pass=${RPCPASS} ServerPort=${RPCPORT} ServerHost=0.0.0.0" >> /opt/metasploit-framework/msfconsole.rc

# Optionally, create a working directory
WORKDIR /workspace/eshuCLP
COPY ./src/ /workspace/eshuCLP/

# Install Eshu using pip based on the pyproject.toml file
RUN python3 -m pip install --upgrade pip setuptools
RUN pip install .

WORKDIR /workspace

EXPOSE 80 4444 8080 55552 55553

# What we are going to do instead is just start the operator container.
ENTRYPOINT ["/bin/bash", "-i"]

# Default command to keep the container running for interactive use. This will cause interacting with it to fail
#ENTRYPOINT ["/bin/bash", "-c", "cd /opt/metasploit-framework && msfconsole -r msfconsole.rc & tail -f /dev/null"]

#ENTRYPOINT ["/bin/bash", "-c", "cd /opt/metasploit-framework && msfconsole -r msfconsole.rc"]
#CMD ["/bin/bash", "-c"]
