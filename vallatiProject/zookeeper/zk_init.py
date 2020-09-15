import logging
import sys
from kazoo.client import KazooClient

logging.basicConfig(level=logging.DEBUG)


if len(sys.argv) < 2:
    print("Not enough input parameters")
    exit(1)

#Create a KazooClient object and establish a connection
zk = KazooClient(hosts=sys.argv[1], read_only=True, logger=logging)
zk.start()

path = "/myApp"

#Store the data
if zk.exists(path):
    zk.delete(path, recursive=True)

zk.ensure_path(path)
zk.create(path+"/broker_addr", b"172.16.2.34") 
zk.create(path+"/broker_port", b"5672")
zk.create(path+"/broker_user", b"root")
zk.create(path+"/broker_psw", b"root")
zk.create(path+"/db_addr", b"172.16.2.57")
zk.create(path+"/db_user", b"root")
zk.create(path+"/db_psw", b"newpassword")
zk.create(path+"/db_name", b"mails")

exit(0)
