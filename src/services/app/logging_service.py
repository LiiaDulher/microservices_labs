from src.services.app.server import Server


class LoggingServer(Server):
    def __init__(self, number):
        super().__init__("LoggingServer"+str(number))

        @self.app.route("/")
        def hello():
            return "<p>Hello, {}</p>".format(self.name)
