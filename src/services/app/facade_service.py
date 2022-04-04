import random
import requests
import time

from flask import request, Response
from threading import Thread

from src.services.app.server import Server


class FacadeServer(Server):
    def __init__(self):
        super().__init__("FacadeService")
        self.log_server = []
        self.log_servers_removed = []
        self.msg_server = None
        self.uuid = 0
        self.shutdown = False
        self.updater = Thread(target=self.update_log_services)
        self.updater.daemon = True
        self.updater.start()

        @self.app.route("/", methods=['POST', 'GET'])
        def facade():
            if request.method == 'POST':
                msg = request.json["msg"]
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
            elif request.method == 'GET':
                response1 = self.get_request(self.msg_server, "Message")
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
                if response1.status_code != 200 or response2.status_code != 200:
                    return Response("Internal Server Error", 500)
                text = response2.text + response1.text
                return Response(text, 200)

    def __del__(self):
        self.shutdown = True
        self.updater.join()

    def add_logging_server(self, log_path):
        self.log_server.append(log_path)

    def add_messages_server(self, msg_path):
        self.msg_server = msg_path

    def remove_logging_server(self, log_path):
        self.log_server.remove(log_path)
        self.log_servers_removed.append(log_path)

    def update_log_services(self):
        while not self.shutdown:
            time.sleep(10)
            restored = []
            for server in self.log_servers_removed:
                try:
                    response = requests.get(server)
                except requests.exceptions.RequestException as err:
                    continue
                if response.status_code == 200:
                    self.add_logging_server(server)
                    restored.append(server)
            for server in restored:
                self.log_servers_removed.remove(server)

    def choose_random_logging_server(self):
        return random.choice(self.log_server)

    def post_request(self, server, msg):
        i = 0
        data = {"uuid": self.uuid + 1, "msg": msg}
        try:
            response = requests.post(server, json=data)
        except requests.exceptions.RequestException as err:
            print("Logging service error:", err)
            return Response("Internal Service Error", 500)
        while i < 10:
            if response.status_code == 200:
                break
            elif response.status_code == 409:
                self.uuid += 10
                i += 1
            else:
                print("Logging service POST request error:", response.status_code, response.text)
                return Response("Internal Service Error", 500)
            data = {"uuid": self.uuid + 1, "msg": msg}
            try:
                response = requests.post(server, json=data)
            except requests.exceptions.RequestException as err:
                print("Logging service error:", err)
                return Response("Internal Service Error", 500)
        self.uuid += 1
        return Response("Message successfully posted", 200)

    def get_request(self, server, server_type):
        try:
            response = requests.get(server)
        except requests.exceptions.RequestException as err:
            print(server_type, "service error:", err)
            return Response("Internal Server Error", 500)
        if response.status_code != 200:
            print(server_type, "service GET request error:", response.status_code, response.text)
            return Response("Internal Server Error", 500)
        return response
