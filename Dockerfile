FROM ubuntu:latest
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get autoremove -y
RUN apt-get install -y git
RUN apt-get install -y make
RUN apt-get install -y mpich
WORKDIR /home
RUN git clone https://github.com/prlahur/testmpi.git
WORKDIR /home/testmpi
RUN make
