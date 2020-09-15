import kazoo
from kazoo.client import KazooClient
import mysql.connector
import pika


brokerAddr = ""
brokerPort = ""
brokerUser = ""
brokerPsw = ""
brokerConn = ""
brokerChan = ""

db_addr = ""
db_user = ""
db_psw = ""
db_name = ""


# CONNECT/DISCONNECT METHODS
def connect():
  try:
    mydb = mysql.connector.connect(
      host=db_addr,
      user=db_user,
      password=db_psw,
      database=db_name
    )
    return mydb
  except mysql.connector.Error as err:
    print("Something went wrong: {}".format(err))
    return None


def disconnect(mydb):
    mydb.close()



# METHODS TO WORK ON THE DB
def postMail(mydb, sender, receiver, text):
  if(mydb == None):
    print("connessione none")
  mycursor = mydb.cursor()
  sql = "INSERT INTO mails (sender, receiver, mailText) VALUES (%s, %s, %s);"
  val = (sender, receiver, text)
  try:
    mycursor.execute(sql, val)
    mydb.commit()
    return True
  except mysql.connector.Error as e:
    mydb.rollback()
    return False


def deleteMail(mydb, id):
  mycursor = mydb.cursor()
  sql =  "DELETE FROM mails WHERE mails.id = %s";
  val = (str(id))
  try:
    mycursor.execute(sql, val)
    mydb.commit()
    return True
  except mysql.connector.Error as e:
    mydb.rollback()
    return False


def getMail(mydb, id):
  mycursor = mydb.cursor()
  sql = "SELECT * FROM mails WHERE id = %s"
  val = (str(id))
  try:
    mycursor.execute(sql, val)
    rowcount = mycursor.rowcount
    if rowcount == 0:
      return None
    else:
      return mycursor.fetchall()
      
  except mysql.connector.Error as e:
    return None


def putMail(mydb, id, sender, receiver, text):
  try:
    intID = int(id)
  except ValueError:
    return -1

  mycursor = mydb.cursor()
  sql = "UPDATE mails SET sender = %s, receiver = %s, mailText = %s WHERE mails.id = %s;"
  val = (sender, receiver, text, str(id))
  mycursor.execute(sql, val)
  mydb.commit()
  rowcount = mycursor.rowcount
  if rowcount == 0:
    return -2
  else:
    return rowcount



def callback(ch, method, properties, body):
    params = body.decode().split('//')
    print('callback')
    
    db = connect()
    stringQueue = params[len(params)-1]
    ch.queue_declare(stringQueue)
    
    if(params[0] == 'create'):
        if(len(params) == 5):
          print('create')
          created = postMail(db, params[1], params[2], params[3])
          ch.basic_publish(exchange = '', routing_key = stringQueue, body = '{"created": ' + str(created) + '}')
    
    elif(params[0] == 'update'):
        if(len(params) == 6):
            print('update')
            updated = putMail(db, params[1], params[2], params[3], params[4])
            ch.basic_publish(exchange = '', routing_key = stringQueue, body = '{"updated": ' + str(updated) + '}')
            
    elif(params[0] == 'delete'):
        if(len(params) == 3):
            print('delete')
            deleted = deleteMail(db, params[1])
            ch.basic_publish(exchange = '', routing_key = stringQueue, body = '{"deleted" : ' + str(deleted) + '}')
            
    elif(params[0] == 'read'):
        if(len(params) == 3):
            print('read')
            resultSet = getMail(db, params[1])
            if(resultSet == None):
                ch.basic_publish(exchange = '', routing_key = stringQueue, body = '{"error" : "Empty resultSet"}')
            else:
                for row in resultSet:
                    ch.basic_publish(exchange = '', routing_key = stringQueue, body = '{"id": "' + str(row[0]) + '", "sender": "' + row[1] + '", "receiver": "' + row[2] + '", "mailText": "' + row[3] + '"}')
            
    else:
        ch.basic_publish(exchange = '', routing_key = stringQueue, body = '{"error, command not found"}')

    
    disconnect(db)
    


    


if __name__ == '__main__':
        
    zk = KazooClient(hosts='172.16.3.50:2181,172.16.1.249:2181,172.16.2.57:2181', read_only=True)
    zk.start()
    #parameters for rabbitmq broker
    data, stat = zk.get("/myApp/broker_addr")
    brokerAddr = data.decode("utf-8")
    data, stat = zk.get("/myApp/broker_port")
    brokerPort = data.decode("utf-8")
    data, stat = zk.get("/myApp/broker_user")

    brokerUser = data.decode("utf-8")
    data, stat = zk.get("/myApp/broker_psw")
    brokerPsw = data.decode("utf-8")
    #parameters to connect the db
    data, stat = zk.get("/myApp/db_addr")
    db_addr = data.decode("utf-8")
    data, stat = zk.get("/myApp/db_user")
    db_user = data.decode("utf-8")
    data, stat = zk.get("/myApp/db_psw")
    db_psw = data.decode("utf-8")
    data, stat = zk.get("/myApp/db_name")
    db_name = data.decode("utf-8")
    
    zk.stop()
    
    
    credentials = pika.PlainCredentials(brokerUser, brokerPsw)
    parameters = pika.ConnectionParameters(brokerAddr, brokerPort, '/', credentials)
    brokerConn = pika.BlockingConnection(parameters)
    brokerChan = brokerConn.channel()
    
    brokerChan.queue_declare(queue='tasks')
    brokerChan.basic_consume(queue='tasks', on_message_callback=callback, auto_ack=True)
    print('Backend is running')
    brokerChan.start_consuming()
    

    
    
