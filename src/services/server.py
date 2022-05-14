from flask import Flask


class Server:

    def __init__(self, name):
        self.app = Flask(name)
        self.name = name

    def run(self, host, port):
        self.app.run(host=host, port=port)

