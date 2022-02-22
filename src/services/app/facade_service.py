from src.services.app.server import Server
from flask import request, Response
import requests


class FacadeServer(Server):
    def __init__(self):
        super().__init__("FacadeService")
        self.log_server = None
        self.msg_server = None
        self.uuid = 0

        @self.app.route("/", methods=['POST', 'GET'])
        def facade():
            if request.method == 'POST':
                msg = request.json["msg"]
                data = {"uuid": self.uuid+1, "msg": msg}
                response = requests.post(self.log_server, json=data)
                self.uuid += 1
                return Response("Message successfully posted", 200)
            elif request.method == 'GET':
                response1 = requests.get(self.msg_server)
                response2 = requests.get(self.log_server)
                text = response2.text + response1.text
                return Response(text, 200)

    def add_logging_server(self, log_path):
        self.log_server = log_path

    def add_messages_server(self, msg_path):
        self.msg_server = msg_path

