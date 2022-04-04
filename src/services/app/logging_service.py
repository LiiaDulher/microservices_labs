from src.services.app.server import Server
from src.data.data_storage import DataStorage
from flask import request, Response


class LoggingServer(Server):
    def __init__(self, number, storage_node):
        super().__init__("LoggingServer"+str(number))
        self.storage = DataStorage(storage_node)
        self.facade_server = None

        @self.app.route("/", methods=['POST', 'GET'])
        def log_request():
            if request.method == 'POST':
                uuid = request.json["uuid"]
                msg = request.json["msg"]
                try:
                    self.storage.save_data(uuid, msg)
                    print(msg)
                    return Response("Ok", 200)
                except KeyError as k:
                    return Response(str(k), 409)
            elif request.method == 'GET':
                return Response(self.storage.get_all_data(), 200)

    def add_facade_server(self, facade_path):
        self.facade_server = facade_path
