from flask import Flask


class Server:

    def __init__(self, name, host, port):
        self.app = Flask(name)
        self.name = name
        self.host = host
        self.port = port

    def run(self):
        self.app.run(host=self.host, port=self.port)

