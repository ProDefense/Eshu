# Start with the Ubuntu 22.04 base image
FROM ubuntu:22.04

# Set the non-interactive mode for apt
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and install necessary packages
RUN apt-get update && apt-get install -y \
    python3 python3-pip vim curl wget bash nmap netcat \
    hydra ruby ruby-dev build-essential iproute2 net-tools\
    openssl libreadline-dev zlib1g-dev libpcap-dev git \
    lsb-release software-properties-common \
    iputils-ping iputils-tracepath iputils-arping dnsutils \
    openssh-server ruby-full libssl-dev \
    libsqlite3-dev libpq-dev libyaml-dev \
    libxml2-dev libxslt1-dev \
    libcurl4-openssl-dev libgmp-dev sudo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set Python3 as the default Python command
RUN ln -sf python3 /usr/bin/python

# Set the default shell to Bash
SHELL ["/bin/bash", "-c"]

RUN git clone https://github.com/rapid7/metasploit-framework.git /opt/metasploit-framework && \
    cd /opt/metasploit-framework && \
    git submodule init && \
    git submodule update && \
    gem install bundler && \
    bundle install

ENV PATH="/opt/metasploit-framework/:$PATH"

# Run the msfconsole.rc commands and start Metasploit RPC service
COPY config_files/msfconsole.rc /opt/metasploit-framework/msfconsole.rc
RUN echo "load msgrpc Pass=${RPCPASS} ServerPort=${RPCPORT} ServerHost=0.0.0.0" >> /opt/metasploit-framework/msfconsole.rc

# Optionally, create a working directory
WORKDIR /workspace

EXPOSE 80 4444 5000 8080 55552 55553

# Default command to keep the container running for interactive use
ENTRYPOINT ["/bin/bash", "-c", "cd /opt/metasploit-framework && msfconsole -r msfconsole.rc & tail -f /dev/null"]

#ENTRYPOINT ["/bin/bash", "-c", "cd /opt/metasploit-framework && msfconsole -r msfconsole.rc"]
# CMD ["/bin/bash"]
