From frolvlad/alpine-python2
RUN apk --update add gcc python-dev musl-dev
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
ENTRYPOINT ["yowsup-cli"]