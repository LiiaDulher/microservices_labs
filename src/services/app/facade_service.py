from src.services.app.server import Server
from flask import request, Response
import requests


class FacadeServer(Server):
    def __init__(self):
        super().__init__("FacadeService")
        self.log_server = None
        self.msg_server = None
        self.uuid = 0

        @self.app.route("/", methods=['POST', 'GET'])
        def facade():
            if request.method == 'POST':
                msg = request.json["msg"]
                i = 0
                data = {"uuid": self.uuid + 1, "msg": msg}
                try:
                    response = requests.post(self.log_server, json=data)
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
                        response = requests.post(self.log_server, json=data)
                    except requests.exceptions.RequestException as err:
                        print("Logging service error:", err)
                        return Response("Internal Service Error", 500)
                self.uuid += 1
                return Response("Message successfully posted", 200)
            elif request.method == 'GET':
                try:
                    response1 = requests.get(self.msg_server)
                except requests.exceptions.RequestException as err:
                    print("Message service error:", err)
                    return Response("Internal Server Error", 500)
                try:
                    response2 = requests.get(self.log_server)
                except requests.exceptions.RequestException as err:
                    print("Logging service error:", err)
                    return Response("Internal Server Error", 500)
                if response1.status_code != 200:
                    print("Message service GET request error:", response1.status_code, response1.text)
                if response2.status_code != 200:
                    print("Logging service GET request error:", response2.status_code, response2.text)
                if response1.status_code != 200 or response2.status_code != 200:
                    return Response("Internal Server Error", 500)
                text = response2.text + response1.text
                return Response(text, 200)

    def add_logging_server(self, log_path):
        self.log_server = log_path

    def add_messages_server(self, msg_path):
        self.msg_server = msg_path

