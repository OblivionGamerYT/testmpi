FROM ubuntu:latest
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get autoremove -y
RUN apt-get install -y make
RUN apt-get install -y mpich
RUN make
