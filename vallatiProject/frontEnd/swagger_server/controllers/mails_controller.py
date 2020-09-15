import connexion
import six
import pika
import socket

from swagger_server.models.mail import Mail  # noqa: E501
from swagger_server import util


def reconnect_to_broker():
    credentials = pika.PlainCredentials(util.brokerUser, util.brokerPsw)
    parameters = pika.ConnectionParameters(util.brokerAddr, util.brokerPort, '/', credentials)
    
    util.brokerConn = pika.BlockingConnection(parameters)
    util.brokerChan = util.brokerConn.channel()
    
    
def callback(ch, method, properties, body):
    util.responseMsg = body.decode()
    print(util.responseMsg)
    ct = ch.consumer_tags[0]
    ch.basic_cancel(consumer_tag=ct)
    

def addmail(body):  # noqa: E501
    """Add a new mail

     # noqa: E501

    :param body: mail data
    :type body: dict | bytes

    :rtype: None
    """

    if connexion.request.is_json:
        try:
            result_queue = "results" + util.myAddr
            body = Mail.from_dict(connexion.request.get_json())  # noqa: E501
            message = "create//{}//{}//{}//{}".format(body.sender, body.receiver, body.mail_text,result_queue)
            
            util.brokerChan.queue_declare(queue='tasks')
            util.brokerChan.basic_publish(exchange='', routing_key='tasks', body=message)

            
            util.brokerChan.queue_declare(queue=result_queue)
            util.brokerChan.basic_qos(prefetch_count=1)
            util.brokerChan.basic_consume(queue=result_queue, on_message_callback=callback, auto_ack=True)
            util.brokerChan.start_consuming()
            
            return util.responseMsg
        except ValueError:
            return 'Invalid input', 405
        except pika.exceptions.StreamLostError:
            reconnect_to_broker()
            return 'Internal server error', 500

    else:
         return 'Invalid input: Json not recognized', 405
    return 'do some magic!'


def deletemail(mailId):  # noqa: E501
    """Deletes an mail

     # noqa: E501

    :param mailId: mail id to delete
    :type mailId: int

    :rtype: None
    """
    if mailId < 0:
        return 'Invalid input', 405
    
    try:
        result_queue = "results" + util.myAddr
        message = "delete//{}//{}".format(mailId, result_queue)
        
        util.brokerChan.queue_declare(queue='tasks')
        util.brokerChan.basic_publish(exchange='', routing_key='tasks', body=message)

        
        util.brokerChan.queue_declare(queue=result_queue)
        util.brokerChan.basic_qos(prefetch_count=1)
        util.brokerChan.basic_consume(queue=result_queue, on_message_callback=callback, auto_ack=True)
        util.brokerChan.start_consuming()
        
        return util.responseMsg
        
    except ValueError:
        return 'Invalid input', 405
    except pika.exceptions.StreamLostError:
        reconnect_to_broker()
        return 'Internal server error', 500


def getmail_by_id(mailId):  # noqa: E501
    """Find mail by ID

    Returns a single mail # noqa: E501

    :param mailId: ID of mail to return
    :type mailId: int

    :rtype: Mail
    """
    if mailId < 0:
        return 'Invalid input', 405
    
    try:
        result_queue = "results" + util.myAddr
        message = "read//{}//{}".format(mailId, result_queue)
        
        util.brokerChan.queue_declare(queue='tasks')
        util.brokerChan.basic_publish(exchange='', routing_key='tasks', body=message)

        
        util.brokerChan.queue_declare(queue=result_queue)
        util.brokerChan.basic_qos(prefetch_count=1)
        util.brokerChan.basic_consume(queue=result_queue, on_message_callback=callback, auto_ack=True)
        util.brokerChan.start_consuming()
        
        return util.responseMsg
        
    except ValueError:
        return 'Invalid input', 405
    except pika.exceptions.StreamLostError:
        reconnect_to_broker()
        return 'Internal server error', 500


def updatemail(mailId,body):
    if connexion.request.is_json:
        try:
            result_queue = "results" + util.myAddr
            
            body = Mail.from_dict(connexion.request.get_json())  # noqa: E501
            message = "update//{}//{}//{}//{}//{}".format(mailId,body.sender, body.receiver, body.mail_text, result_queue)
            util.brokerChan.queue_declare(queue='tasks')
            util.brokerChan.basic_publish(exchange='', routing_key='tasks', body=message)

            
            util.brokerChan.queue_declare(queue=result_queue)
            util.brokerChan.basic_qos(prefetch_count=1)
            util.brokerChan.basic_consume(queue=result_queue, on_message_callback=callback, auto_ack=True)
            util.brokerChan.start_consuming()
            
            return util.responseMsg
        except ValueError:
            return 'Invalid input', 405
        except pika.exceptions.StreamLostError:
            reconnect_to_broker()
            return 'Internal server error', 500

    else:
         return 'Invalid input: Json not recognized', 405
    return 'do some magic!'

