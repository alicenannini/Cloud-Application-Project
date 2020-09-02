
import mysql.connector
import pika


brokerAddr = ""
brokerConn = ""
brokerChan = ""


# CONNECT/DISCONNECT METHODS
def connect():
  try:
    mydb = mysql.connector.connect(
      host='172.16.2.57',
      user='root',
      password='newpassword',
      database='mails'
    )
    return mydb
  except mysql.connector.Error as err:
    print("Something went wrong: {}".format(err))
    return None
    


def disconnect(mydb):
    mydb.close()



def getMails(mydb):
  mycursor = mydb.cursor()
  mycursor.execute("SELECT id FROM mails")
  return mycursor.fetchall()



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
  val = (str(id),)
  try:
    mycursor.execute(sql, val)
    mydb.commit()
    return True
  except mysql.connector.Error as e:
    mydb.rollback()
    return False

# ----------------------------------------------------------------------------------------------------------------------

def getMail(mydb, id):
  mycursor = mydb.cursor()
  sql = "SELECT * FROM mails WHERE id = %s"
  val = (str(id),)
  try:
    mycursor.execute(sql, val)
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
        #if(len(params) == 5):
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
    
   
def main():
    brokerChan.queue_declare(queue='tasks')
    brokerChan.basic_consume(queue='tasks', on_message_callback=callback, auto_ack=True)
    print('Back-end ready.')
    brokerChan.start_consuming()


if __name__ == '__main__':
    credentials = pika.PlainCredentials("root", "root")
    brokerAddr = "172.16.2.34"
    parameters = pika.ConnectionParameters(brokerAddr, '5672', '/', credentials)
    brokerConn = pika.BlockingConnection(parameters)
    brokerChan = brokerConn.channel()
    main()


    
    
