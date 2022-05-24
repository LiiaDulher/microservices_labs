import consul

from flask import request, Response

from services.server import Server
from src.data.distributed_map import DistributedMap
from src.data.exceptions.hazelcast_unavailable_error import HazelcastUnavailable


class LoggingServer(Server):
    def __init__(self, number, host, port):
        super().__init__("LoggingServer" + str(number), host, port)
        self.number = number
        self.consul = consul.Consul()
        self.map_name = None
        self.storage_node = None
        self.get_map_info()
        self.storage = DistributedMap(self.storage_node, self.map_name)
        self.facade_server = []
        self.register_myself()
        self.get_facade_server()

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

    def __del__(self):
        self.consul.agent.service.deregister(self.name)

    def register_myself(self):
        url = "http://" + self.host + ":" + self.port + "/health"
        address = self.host + ":" + self.port
        self.consul.agent.service.register(name='logging-service', service_id=self.name, address=address,
                                           check=consul.Check.http(url=url, interval='10s'))

    def get_facade_server(self):
        services = self.consul.agent.services()
        for server_name in services.keys():
            if services[server_name]['Service'] == 'facade-service':
                self.facade_server.append(services[server_name]['Address'])

    def get_map_info(self):
        index, data = self.consul.kv.get('hazelcast-map-name')
        self.map_name = data['Value'].decode('utf-8')

        index, data = self.consul.kv.get('hazelcast-client-' + str(self.number))
        self.storage_node = data['Value'].decode('utf-8')
