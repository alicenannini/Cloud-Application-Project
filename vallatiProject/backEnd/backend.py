
import mysql.connector

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



def callback():




def main():
    db = connect()
    postMail(db, 'Ste', 'Ma', 'ciaone proprio')

if __name__ == "__main__":
    main()
    
    
    
    
