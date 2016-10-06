FROM debian
RUN apt-get update
RUN apt-get install -y python
RUN apt-get install -y python-pip
RUN pip install yowsup2