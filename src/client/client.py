import requests


class Client:
    def __init__(self, name):
        self.name = name
        self.url = None

    def add_web_server(self, url):
        self.url = url

    def post_message(self, msg):
        data = {"msg": msg}
        try:
            response = requests.post(self.url, json=data)
        except requests.exceptions.RequestException as err:
            return 0, err
        return response.status_code, response.text

    def get_data(self):
        try:
            response = requests.get(self.url)
        except requests.exceptions.RequestException as err:
            return 0, err
        return response.status_code, response.text
