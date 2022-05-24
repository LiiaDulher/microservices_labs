import consul
import time

from flask import request, Response
from threading import Thread

from src.data.exceptions.hazelcast_unavailable_error import HazelcastUnavailable
from src.data.distributed_queue import DistributedQueue
from src.data.local_map import LocalMap
from services.server import Server


class MessageServer(Server):
    def __init__(self, number, host, port):
        super().__init__("MessageServer" + str(number), host, port)
        self.consul = consul.Consul()
        self.register_myself()
        self.facade_server = []
        self.get_facade_server()
        self.storage = LocalMap()
        self.queue_name = None
        self.get_queue_info()
        self.queue = DistributedQueue(self.queue_name)
        self.id = 0
        self.shutdown = False
        self.queue_msg = Thread(target=self.post_msg)
        self.queue_msg.daemon = True
        self.queue_msg.start()

        @self.app.route("/", methods=['GET'])
        def msg_request():
            if request.method == 'GET':
                values = self.storage.get_all_data()
                return Response(values, 200)

        @self.app.route("/health", methods=['GET'])
        def health_check():
            return Response("healthy", 200)

    def __del__(self):
        self.shutdown = True
        self.consul.agent.service.deregister(self.name)
        self.queue_msg.join()

    def get_facade_server(self):
        services = self.consul.agent.services()
        for server_name in services.keys():
            if services[server_name]['Service'] == 'facade-service':
                self.facade_server.append('http://' + services[server_name]['Address'] + '/')

    def get_queue_info(self):
        index, data = self.consul.kv.get('hazelcast-queue-name')
        self.queue_name = data['Value'].decode('utf-8')

    def register_myself(self):
        url = "http://" + self.host + ":" + self.port + "/health"
        address = self.host + ":" + self.port
        self.consul.agent.service.register(name='messages-service', service_id=self.name, address=address,
                                           check=consul.Check.http(url=url, interval='10s'))

    def post_msg(self):
        while not self.shutdown:
            time.sleep(10)
            try:
                if not self.queue.is_empty():
                    try:
                        msg = self.queue.get_data()
                        print(msg)
                        self.storage.save_data(self.id, msg)
                        self.id += 1
                    except HazelcastUnavailable as err:
                        print(err)
            except HazelcastUnavailable as err:
                print(err)

