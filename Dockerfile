FROM python:2.7
WORKDIR /app
ADD . .
RUN  python setup.py install
RUN rm -rf *