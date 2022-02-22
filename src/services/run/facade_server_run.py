from src.services.app.facade_service import FacadeServer


def main():
    server = FacadeServer()
    server.add_logging_server("http://127.0.0.1:8001/")
    server.add_messages_server("http://127.0.0.1:8002/")
    server.run("127.0.0.1", 8000)


if __name__ == "__main__":
    main()
