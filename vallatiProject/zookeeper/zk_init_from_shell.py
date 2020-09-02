from kazoo.client import KazooClient

hosts = "172.16.3.50:2181,172.16.1.249:2181,172.16.2.57:2181"

zk = KazooClient(hosts=hosts, read_only=True)
zk.start()

path = "/myApp"

#Store the data
if zk.exists(path):
    zk.delete(path, recursive=True)

zk.ensure_path(path)
zk.create(path+"/broker_addr", b"172.16.2.57") 
zk.create(path+"/broker_port", b"5672")
zk.create(path+"/broker_user", b"root")
zk.create(path+"/broker_psw", b"root")
zk.create(path+"/db_addr", b"172.16.2.57")
zk.create(path+"/db_user", b"root")
zk.create(path+"/db_psw", b"newpassword")
zk.create(path+"/db_name", b"mails")

exit(0)
