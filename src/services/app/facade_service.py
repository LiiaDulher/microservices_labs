from src.services.app.server import Server


class FacadeServer(Server):
    def __init__(self):
        super().__init__("FacadeService")

        @self.app.route("/")
        def hello():
            return "<p>Hello, {}</p>".format("facade")
