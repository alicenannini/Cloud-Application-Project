# Cloud-Application-Project
## Guidelines
Design and develop a multi-tier cloud computing application based on containers. The application should
mimic a certain application implementing some simple functionalities. The cloud computing application will
need the following components:
- A load balancer layer to load-balance ingress traffic implemented using the software HAproxy
- A frontend layer exposing a REST interface that receives and dispatches requests
- A backend layer that processes the requests coming from the frontend
- A database layer that stores the data

The user can interact with the application through the REST plugin installed on the browser.
The user will be able to perform the retrieval of some data. The backend must process the requests from
users by interacting with the database.
In order to ensure scalability a message-based queue system must be used for the communication between
the frontend and the backend.
Configuration parameters shared across all the components of the application should be stored in a
Zookeeper instance running in a container.
#### References
- HAproxy docker image: https://hub.docker.com/_/haproxy
- HAproxy configuration: https://dzone.com/articles/how-to-configure-ha-proxy-as-a-proxy-and-loadbalan
- Zookeeper container: https://hub.docker.com/_/zookeeper
- Python Kazoo library to interact with Zookeeper: https://kazoo.readthedocs.io/en/latest/basic_usage.html#creating-nodes

## Containers location
172.16.1.249: myfe, myzk-2
172.16.2.34: mymb, haproxy
172.16.2.57: myfe, mybe, mydb, myzk-3
172.16.3.50: mybe, myzk-1
