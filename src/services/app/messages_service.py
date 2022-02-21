from src.services.app.server import Server


class MessageServer(Server):
    def __init__(self, number):
        super().__init__("MessageServer"+str(number))

        @self.app.route("/")
        def hello():
            return "<p>Hello, {}</p>".format(self.name)
