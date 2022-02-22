import requests


class Client:
    def __init__(self, name):
        self.name = name
        self.url = None

    def add_web_server(self, url):
        self.url = url

    def post_message(self, msg):
        data = {"msg": msg}
        response = requests.post(self.url, json=data)
        if response:
            return True
        return False

    def get_data(self):
        response = requests.get(self.url)
        return response.text
