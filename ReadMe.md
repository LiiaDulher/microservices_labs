# Microservices 
## Team: [Liia Dulher](https://github.com/LiiaDulher)
### Usage
Please add project source directory to <b>PYTHONPATH</b> in order for imports to work.

Run Hazelcast nodes before logging services, that use it.<br>
Run Hazelcast nodes before messaging services, that use it.

Start consul before all other services.<br>
Run <b>consul.kv.py</b> to put all values into consul key-value storage.<br>
````
python src/services/consul_service/consul_kv.py
````
Please put all new hazelcast nodes addresses into kv with key 'hazelcast-client-N', 
where N is number of node. Notice, that each logging-server wants node with the same number.

Run all services using their runners.
You can do it using default settings:
````
python src/services/facade_service/facade_server_run.py
python src/services/logging_service/logging_server_run.py
python src/services/messages_service/messages_server_run.py
````
or customize:
````
python src/services/facade_service/facade_server_run.py number server_host server_port
python src/services/facade_service/facade_server_run.py 1 127.0.0.1 8000
````
````
python src/services/logging_service/logging_server_run.py server_number server_host server_port
python src/services/logging_service/logging_server_run.py 1 127.0.0.1 8001
````
````
python src/services/messages_service/messages_server_run.py server_number server_host server_port
python src/services/messages_service/messages_server_run.py 2 127.0.0.1 8002
````

You send <b>POST</b> or <b>GET</b> HTTP requests to facade services.
#### Important!
GET request does not require parameters.<br>
POST request must have <b>json</b> body with field <b>msg</b> inside.<br>
Example of POST request body.
````
{
    "msg": "Hello world!"
}
````

By running main.py you can use my client for sending requests.<br>
Example of usage:
````
Enter client's name: Liia
Please choose one of the options or 'end' to exit

'Post' or 'Get': post
Enter message: msg1
Message successfully posted.

'Post' or 'Get': get
msg1
msg1

'Post' or 'Get': post
Enter message: msg2
Message successfully posted.

'Post' or 'Get': post
Enter message: msg3
Message successfully posted.

'Post' or 'Get': get
msg1
msg2
msg3
msg2

'Post' or 'Get': get
msg1
msg2
msg3
msg1
msg3

'Post' or 'Get': end
````