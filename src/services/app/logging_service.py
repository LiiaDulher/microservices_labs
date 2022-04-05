from flask import request, Response

from src.data.distributed_map import DistributedMap
from data.exceptions.hazelcast_unavailable_error import HazelcastUnavailable
from src.services.app.server import Server


class LoggingServer(Server):
    def __init__(self, number, storage_node):
        super().__init__("LoggingServer"+str(number))
        self.storage = DistributedMap(storage_node)
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
                except HazelcastUnavailable as err:
                    return Response(str(err), 500)
            elif request.method == 'GET':
                try:
                    values = self.storage.get_all_data()
                    return Response(values, 200)
                except HazelcastUnavailable as err:
                    return Response(str(err), 500)

    def add_facade_server(self, facade_path):
        self.facade_server = facade_path
