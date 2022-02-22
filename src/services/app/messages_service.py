from src.services.app.server import Server
from flask import request, Response


class MessageServer(Server):
    def __init__(self, number):
        super().__init__("MessageServer"+str(number))
        self.facade_server = None

        @self.app.route("/", methods=['POST', 'GET'])
        def msg_request():
            if request.method == 'POST':
                pass
            elif request.method == 'GET':
                return Response("Not implemented yet", 200)

    def add_facade_server(self, facade_path):
        self.facade_server = facade_path
