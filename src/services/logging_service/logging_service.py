import consul

from flask import request, Response

from services.server import Server
from src.data.distributed_map import DistributedMap
from src.data.exceptions.hazelcast_unavailable_error import HazelcastUnavailable


class LoggingServer(Server):
    def __init__(self, number, host, port, storage_node):
        super().__init__("LoggingServer"+str(number), host, port)
        self.consul = consul.Consul()
        self.storage = DistributedMap(storage_node)
        self.facade_server = None
        self.register_myself()

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

        @self.app.route("/health", methods=['GET'])
        def health_check():
            return Response("healthy", 200)

    def register_myself(self):
        url = "http://" + self.host + ":" + self.port + "/health"
        self.consul.agent.service.register(name='logging-service', service_id=self.name,
                                           check=consul.Check.http(url=url, interval='10s', deregister=True))

    def add_facade_server(self, facade_path):
        self.facade_server = facade_path
