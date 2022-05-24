import consul
import random
import requests
import time

from flask import request, Response
from threading import Thread

from src.data.exceptions.hazelcast_unavailable_error import HazelcastUnavailable
from src.data.distributed_queue import DistributedQueue
from services.server import Server


class FacadeServer(Server):
    def __init__(self, number, host, port):
        super().__init__("FacadeService" + str(number), host, port)
        self.consul = consul.Consul()
        self.register_myself()
        self.log_server = []
        self.log_number = 0
        self.msg_server = []
        self.msg_number = 0
        self.get_services()
        self.uuid = 0
        self.queue = DistributedQueue()
        self.shutdown = False
        print(self.log_server, self.msg_server)
        self.updater = Thread(target=self.update_services)
        self.updater.daemon = True
        self.updater.start()

        @self.app.route("/", methods=['POST', 'GET'])
        def facade():
            if request.method == 'POST':
                msg = request.json["msg"]
                response1 = self.post_on_log_server(msg)
                response2 = self.post_on_msg_server(msg)
                if response1.status_code != 200 or response2.status_code != 200:
                    return Response("Internal Server Error", 500)
                return response1
            elif request.method == 'GET':
                response1 = self.get_from_msg_server()
                response2 = self.get_from_log_server()
                if response1.status_code != 200 or response2.status_code != 200:
                    return Response("Internal Server Error", 500)
                text = response2.text + response1.text
                return Response(text, 200)

        @self.app.route("/health", methods=['GET'])
        def health_check():
            return Response("healthy", 200)

    def __del__(self):
        self.shutdown = True
        self.consul.agent.service.deregister(self.name)
        self.updater.join()

    def register_myself(self):
        url = "http://" + self.host + ":" + self.port + "/health"
        address = self.host + ":" + self.port
        self.consul.agent.service.register(name='facade-service', service_id=self.name, address=address,
                                           check=consul.Check.http(url=url, interval='10s'))

    def remove_logging_server(self, log_path):
        self.log_server.remove(log_path)

    def remove_messages_server(self, msg_path):
        self.msg_server.remove(msg_path)

    def get_services(self):
        services = self.consul.agent.services()
        log_services = []
        msg_services = []
        for server_name in services.keys():
            if services[server_name]['Service'] == 'logging-service':
                log_services.append(services[server_name]['Address'])
            elif services[server_name]['Service'] == 'messages-service':
                msg_services.append(services[server_name]['Address'])
        self.log_server = log_services
        self.msg_server = msg_services
        self.log_number = len(self.log_server)
        self.msg_number = len(self.msg_server)

    def update_services(self):
        while not self.shutdown:
            time.sleep(30)
            if (len(self.log_server) != self.log_number) or (len(self.msg_server) != self.msg_number):
                self.get_services()

    def choose_random_logging_server(self):
        return random.choice(self.log_server)

    def choose_random_message_server(self):
        return random.choice(self.msg_server)

    def post_request(self, server, msg):
        i = 0
        data = {"uuid": self.uuid + 1, "msg": msg}
        try:
            response = requests.post(server, json=data)
        except requests.exceptions.RequestException as err:
            print("Logging service[", server, "]error:", err)
            return Response("Internal Service Error", 500)
        while i < 10:
            if response.status_code == 200:
                break
            elif response.status_code == 409:
                self.uuid += 10
                i += 1
            else:
                print("Logging service[", server, "] POST request error:", response.status_code, response.text)
                return Response("Internal Service Error", 500)
            data = {"uuid": self.uuid + 1, "msg": msg}
            try:
                response = requests.post(server, json=data)
            except requests.exceptions.RequestException as err:
                print("Logging service[", server, "] error:", err)
                return Response("Internal Service Error", 500)
        self.uuid += 1
        return Response("Message successfully posted", 200)

    @staticmethod
    def get_request(server, server_type):
        try:
            response = requests.get(server)
        except requests.exceptions.RequestException as err:
            print(server_type, "service[", server, "] error:", err)
            return Response("Internal Server Error", 500)
        if response.status_code != 200:
            print(server_type, "service[", server, "] GET request error:", response.status_code, response.text)
            return Response("Internal Server Error", 500)
        return response

    def post_on_log_server(self, msg):
        while True:
            try:
                log_server = self.choose_random_logging_server()
            except IndexError:
                return Response("Internal Server Error", 500)
            response = self.post_request(log_server, msg)
            if response.status_code == 200:
                break
            else:
                self.remove_logging_server(log_server)
        return response

    def post_on_msg_server(self, msg):
        try:
            self.queue.put_data(msg)
        except HazelcastUnavailable as err:
            return Response(str(err), 500)
        return Response("Ok", 200)

    def get_from_log_server(self):
        while True:
            try:
                log_server = self.choose_random_logging_server()
            except IndexError:
                response2 = Response("Internal Server Error", 500)
                break
            response2 = self.get_request(log_server, "Logging")
            if response2.status_code == 200:
                break
            else:
                self.remove_logging_server(log_server)
        return response2

    def get_from_msg_server(self):
        while True:
            try:
                msg_server = self.choose_random_message_server()
            except IndexError:
                response1 = Response("Internal Server Error", 500)
                break
            response1 = self.get_request(msg_server, "Message")
            if response1.status_code == 200:
                break
            else:
                self.remove_messages_server(msg_server)
        return response1
