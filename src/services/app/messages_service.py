import time

from flask import request, Response
from threading import Thread

from src.data.distributed_queue import DistributedQueue
from src.data.local_map import LocalMap
from src.services.app.server import Server


class MessageServer(Server):
    def __init__(self, number):
        super().__init__("MessageServer"+str(number))
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
                return Response("Not implemented yet", 200)

    def __del__(self):
        self.shutdown = True
        self.queue_msg.join()

    def add_facade_server(self, facade_path):
        self.facade_server = facade_path

    def post_msg(self):
        while not self.shutdown:
            time.sleep(10)

