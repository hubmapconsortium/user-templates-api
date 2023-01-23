FROM python:3.8-buster
WORKDIR /code
ENV PYTHONUNBUFFERED=1
# TODO: added RUN to create tmp dir but not sure if needed,
# or if RUN on line 9 should just install in current dir
RUN /bin/bash -c 'mkdir tmp'
COPY requirements.txt /tmp/
RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt
RUN apt-get update && \
    apt-get install -y sudo && \
    apt-get install -y virtualenv && \
    rm -rf /var/lib/apt/lists/*
