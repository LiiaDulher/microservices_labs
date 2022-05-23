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
        super().__init__("MessageServer"+str(number), host, port)
        self.consul = consul.Consul()
        self.register_myself()
        self.facade_server = None
        self.storage = LocalMap()
        self.queue = DistributedQueue()
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
        self.queue_msg.join()

    def add_facade_server(self, facade_path):
        self.facade_server = facade_path

    def register_myself(self):
        url = "http://" + self.host + ":" + self.port + "/health"
        self.consul.agent.service.register(name='messages-service', service_id=self.name,
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

