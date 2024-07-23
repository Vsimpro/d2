FROM ubuntu:22.04

WORKDIR /root
COPY . /root
RUN mkdir /root/temp

#
#   Configure the System
#

ENV TZ=Europe/London
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
ARG DEBIAN_FRONTEND=noninteractive

# Update
RUN apt -y update && DEBIAN_FRONTEND=noninteractive apt -y dist-upgrade && apt -y autoremove && apt clean
RUN apt install --reinstall coreutils
RUN apt -y install golang-go python3 python3-pip git wget unzip file zip grep coreutils


# Configure Go
RUN export GOPATH=$HOME/go
RUN export GOROOT=/usr/local/go
RUN export PATH=$GOPATH/bin:$GOROOT/bin:$PATH

RUN mkdir -p ${GOPATH}/src ${GOPATH}/bin

#
#   Install the tools
#

# Install nmap
RUN apt install nmap -y

#   Install Nuclei 
RUN wget https://github.com/projectdiscovery/nuclei/releases/download/v3.2.8/nuclei_3.2.8_linux_amd64.zip
RUN unzip -o nuclei_*_linux_amd64.zip
RUN chmod u+x nuclei

# Install Subfinder 
RUN wget https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip
RUN unzip -o subfinder_*_linux_amd64.zip
RUN chmod u+x subfinder

# Install Feroxbuster
RUN wget https://github.com/epi052/feroxbuster/releases/latest/download/feroxbuster_amd64.deb.zip
RUN unzip feroxbuster_amd64.deb.zip
RUN apt install ./feroxbuster_*_amd64.deb

#
#   Install all the needed Wordlists
#

# Install SecLists
RUN wget -c https://github.com/danielmiessler/SecLists/archive/master.zip -O SecList.zip
RUN unzip SecList.zip
RUN mkdir /usr/share/seclists
RUN mv SecLists-master/* /usr/share/seclists

# Install Wordlists
RUN wget https://raw.githubusercontent.com/daviddias/node-dirbuster/master/lists/directory-list-2.3-big.txt
RUN wget https://raw.githubusercontent.com/v0re/dirb/master/wordlists/common.txt

# Install Python libraries
RUN apt-get install python3-pip
RUN python3 -m pip install python-dotenv
RUN python3 -m pip install discord_webhook
RUN python3 -m pip install discord.py 

CMD ["python3", "main.py"]