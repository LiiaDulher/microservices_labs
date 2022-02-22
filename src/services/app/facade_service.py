from src.services.app.server import Server
from flask import request, render_template
import requests


class FacadeServer(Server):
    def __init__(self):
        super().__init__("FacadeService")
        self.log_server = None
        self.msg_server = None

        @self.app.route("/")
        def hello():
            # if request.method == 'POST':
            #     pass
            # elif request.method == 'GET':
            #     pass
            # else:
            #     pass
            # data = {"uuid": "12", "msg": "text"}
            # url = self.log_server
            # response = requests.post(url, json=data)
            # print(response.text)
            response = requests.get(self.msg_server)
            print(response.text)
            return render_template("home.html")

        @self.app.route("/post")
        def post_msg():
            return "<p>Post your message.</p>"

        @self.app.route("/get")
        def get_msg():
            return "<p>Get all messages.</p>"

    def add_logging_server(self, log_path):
        self.log_server = log_path

    def add_messages_server(self, msg_path):
        self.msg_server = msg_path

