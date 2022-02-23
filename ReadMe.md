# Task 1
## Microservices basics
## Team: [Liia Dulher](https://github.com/LiiaDulher)
### Usage
Run all services using their runners.
````
python src/services/run/facade_server_run.py
python src/services/run/logging_server_run.py
python src/services/run/messages_server_run.py
````

You send POST or GET HTTP requests to facade services.
 ````
examples
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