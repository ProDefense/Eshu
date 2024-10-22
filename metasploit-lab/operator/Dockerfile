# Dockerfile Attacker Machine
# usage: docker exec -it operator /bin/bash
# Start with the Ubuntu base image
FROM ubuntu:22.04

# Set non-interactive environment for apt
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    gnupg2 \
    lsb-release \
    software-properties-common \
    apt-transport-https \
    python3 \
    python3-pip \
    build-essential \
    nmap \
    netcat \
    hydra \
    net-tools \
    iputils-ping \
    iputils-tracepath \
    iputils-arping \
    dnsutils \
    openssh-server \
    ruby-full \
    libssl-dev \
    libreadline-dev \
    zlib1g-dev \
    libsqlite3-dev \
    libpq-dev \
    libpcap-dev \
    libyaml-dev \
    libxml2-dev \
    libxslt1-dev \
    libcurl4-openssl-dev \
    libgmp-dev \
    vim \
    sudo \
    supervisor && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

#RUN git config --global http.postBuffer 524288000
# Install Metasploit dependencies
RUN git clone https://github.com/rapid7/metasploit-framework.git /opt/metasploit-framework && \
    cd /opt/metasploit-framework && \
    git submodule init && \
    git submodule update && \
    gem install bundler && \
    bundle install

#RUN service postgresql start
#RUN cd /opt/metasploit-framework && msfdb init

#ENV MSF_DATABASE_CONFIG=/opt/metasploit-framework/config/database.yml
ENV PATH="/opt/metasploit-framework/:$PATH"

#Install Python dependencies for Eshu API
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip3 install --no-cache-dir -r /usr/src/app/requirements.txt

# Clone and add msfrpc manually
RUN git clone https://github.com/SpiderLabs/msfrpc.git /usr/src/app/msfrpc

# Ensure msfrpc is accessible by adding it to the Python path
ENV PYTHONPATH=/usr/src/app/msfrpc:$PYTHONPATH

# Install Havoc C2
#RUN git clone https://github.com/HavocFramework/Havoc /opt/havoc && \
#    cd /opt/havoc && \
#    make all
# RUN git clone https://github.com/ha0ye/Havoc.git && \
#     cd Havoc && \
#     bash install.sh

# Install Sliver C2
#RUN curl https://sliver.sh/install | bash
# RUN git clone https://github.com/BishopFox/sliver.git && \
#     cd sliver && \
#     ./build.sh

# Install Python packages needed for API
#COPY requirements.txt /opt/requirements.txt
#RUN pip3 install -r /opt/requirements.txt

# Copy the Eshu API code into the container
COPY ./api /usr/src/app/api

# Create a directory for persistent data
VOLUME ["/home/msf/.msf4"]

# Copy Python API code
#COPY ./api /opt/api

# Supervisor configuration to run both Metasploit and Eshu API
COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose Ports
EXPOSE 4444 5000 1337 8888

# Run both Metasploit and Eshu API using supervisord
CMD ["/usr/bin/supervisord"]

#ENTRYPOINT ["bash", "-c", "msfdb init && exec msfconsole"]
#ENTRYPOINT ["bash", "-c", "service postgresql start && msfdb init && exec msfconsole"]
# Open Shell
