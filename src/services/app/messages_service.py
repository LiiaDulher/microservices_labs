from flask import request, Response

from src.data.local_map import LocalMap
from src.services.app.server import Server


class MessageServer(Server):
    def __init__(self, number):
        super().__init__("MessageServer"+str(number))
        self.facade_server = None

        @self.app.route("/", methods=['GET'])
        def msg_request():
            if request.method == 'GET':
                return Response("Not implemented yet" + self.name, 200)

    def add_facade_server(self, facade_path):
        self.facade_server = facade_path
