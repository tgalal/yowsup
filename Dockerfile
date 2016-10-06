FROM debian
RUN apt-get update
RUN apt-get install -y python
RUN apt-get install -y python-pip
RUN apt-get install -y python-setuptools
RUN apt-get install -y build-essential 
RUN apt-get install -y git 
RUN git clone https://github.com/tgalal/yowsup
WORKDIR yowsup
RUN apt-get install -y python-dev
RUN pip install --upgrade six
RUN python setup.py install