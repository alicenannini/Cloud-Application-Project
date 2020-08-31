#!/usr/bin/env python3

import connexion
import pika
import logging
from swagger_server import util
from swagger_server import encoder


def main():
    app = connexion.FlaskApp(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Mail REST API'})
    app.run(port=8080)


if __name__ == '__main__':
    logging.debug("avviooooo main")
    credentials = pika.PlainCredentials("root", "root")
    util.brokerAddr = "172.16.2.34"
    parameters = pika.ConnectionParameters(util.brokerAddr, '5672', '/', credentials)
    util.brokerConn = pika.BlockingConnection(parameters)
    util.brokerChan = util.brokerConn.channel()
    main()
