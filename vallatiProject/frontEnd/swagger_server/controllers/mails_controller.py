import connexion
import six

import pika

from swagger_server.models.mail import Mail  # noqa: E501
from swagger_server import util


def reconnect_to_broker():
    util.brokerConn = pika.BlockingConnection(pika.ConnectionParameters(util.brokerAddr))
    util.brokerChan = util.brokerConn.channel()
    
    
def callback(ch, method, properties, body):
    print(body.decode())
    '''
    result.Result.result_msg = body.decode()
    ct = ch.consumer_tags[0]
    ch.basic_cancel(consumer_tag=ct)
    '''


def addmail(body):  # noqa: E501
    """Add a new mail

     # noqa: E501

    :param body: mail data
    :type body: dict | bytes

    :rtype: None
    """



    if connexion.request.is_json:
        try:
            body = Mail.from_dict(connexion.request.get_json())  # noqa: E501
            message = "create//{}//{}//{}".format(body.sender, body.receiver, body.mailText)
            result_queue = "resultsssss"
            config.Config.channel.queue_declare(queue='tasks')
            config.Config.channel.basic_publish(exchange='', routing_key='tasks', body=message)


            '''
            config.Config.channel.queue_declare(queue=result_queue)
            config.Config.channel.basic_qos(prefetch_count=1)
            config.Config.channel.basic_consume(queue=result_queue, on_message_callback=callback, auto_ack=True)
            config.Config.channel.start_consuming()
            '''
            return 'messaggio inviato in coda'
        except ValueError:
            return 'Invalid iiiiiinput', 405
        except StreamLostError:
            reconnect_to_broker()
            return 'Internal server error', 500

    else:
         return 'Invalid inpuuuuuuuuut', 405
    return 'doooooo some magic!'


def deletemail(mailId):  # noqa: E501
    """Deletes an mail

     # noqa: E501

    :param mailId: mail id to delete
    :type mailId: int

    :rtype: None
    """
    
    message = "delete//"
    
    return 'do some magic!'


def getmail_by_id(mailId):  # noqa: E501
    """Find mail by ID

    Returns a single mail # noqa: E501

    :param mailId: ID of mail to return
    :type mailId: int

    :rtype: Mail
    """
    
    message = "read//"
    
    return 'mail_' + str(mailId)


def updatemail(body):  # noqa: E501
    """Update an existing mail

     # noqa: E501

    :param body: mail object that needs to be added to the store
    :type body: dict | bytes

    :rtype: None
    """
    
    message = "update//"
    
    if connexion.request.is_json:
        body = Mail.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def updatemail_with_form(mailId, name=None, status=None):  # noqa: E501
    """Updates an mail in the store with form data

     # noqa: E501

    :param mailId: ID of employe that needs to be updated
    :type mailId: int
    :param name: Updated name of the mail
    :type name: str
    :param status: Updated status of the mail
    :type status: str

    :rtype: None
    """
    return 'do some magic!'

