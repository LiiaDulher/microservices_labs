# Task 4
## Microservices with Messaging queue
## Team: [Liia Dulher](https://github.com/LiiaDulher)
### Usage
Please add project source directory to <b>PYTHONPATH</b> in order for imports to work.

Run Hazelcast nodes before logging services, that use it.
Run Hazelcast noodes before messaging services, that use it.

Run all services using their runners.
You can do it using default settings:
````
python src/services/run/facade_server_run.py
python src/services/run/logging_server_run.py
python src/services/run/messages_server_run.py
````
or customize:
````
python src/services/run/facade_server_run.py server_host server_port logging_server_urls(separated by comas, not spaces) messages_server_urls(separated by comas, not spaces)
python src/services/run/facade_server_run.py 127.0.0.1 8000 http://127.0.0.1:8001/,http://127.0.0.1:8003/,http://127.0.0.1:8004/ http://127.0.0.1:8002/,http://127.0.0.1:8005/
````
````
python src/services/run/logging_server_run.py server_number server_host server_port storage_node_address facade_server_url
python src/services/run/logging_server_run.py 1 127.0.0.1 8001 127.0.0.1:5701 http://127.0.0.1:8000/
````
````
python src/services/run/messages_server_run.py server_number server_host server_port facade_server_url
python src/services/run/messages_server_run.py 2 127.0.0.1 8002 http://127.0.0.1:8000/
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
Not implemented yet

'Post' or 'Get': post
Enter message: msf2
Message successfully posted.

'Post' or 'Get': post
Enter message: msg1
Message successfully posted.

'Post' or 'Get': get
msg1
msf2
msg1
Not implemented yet

'Post' or 'Get': end
````