#!/usr/bin/env python3
from kazoo.client import KazooClient
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
    logging.debug("starting front-end main")
    
    zk = KazooClient(hosts='172.16.3.50:2181,172.16.1.249:2181,172.16.2.57:2181', read_only=True)
    zk.start()
    
    data, stat = zk.get("/myApp/broker_user")
    util.brokerUser = data.decode("utf-8")
    data, stat = zk.get("/myApp/broker_psw")
    util.brokerPsw = data.decode("utf-8")
    credentials = pika.PlainCredentials(util.brokerUser, util.brokerPsw)
    
    data, stat = zk.get("/myApp/broker_addr")
    util.brokerAddr = data.decode("utf-8")
    data, stat = zk.get("/myApp/broker_port")
    util.brokerPort = data.decode("utf-8")
    parameters = pika.ConnectionParameters(util.brokerAddr, util.brokerPort, '/', credentials)
    zk.stop()
    
    util.brokerConn = pika.BlockingConnection(parameters)
    util.brokerChan = util.brokerConn.channel()
    main()
