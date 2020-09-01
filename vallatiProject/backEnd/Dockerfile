FROM python:3-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Pika is the Python implementation of the AMPQ protocol
RUN pip3 install pika

RUN pip3 install mysql-connector-python
RUN pip3 install kazoo

# This variable forces pika to print something out
ENV PYTHONUNBUFFERED=1 

COPY backend.py /usr/src/app

ENTRYPOINT ["python3"]

CMD ["backend.py"]
