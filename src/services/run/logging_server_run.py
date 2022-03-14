from src.services.app.logging_service import LoggingServer
from src.data.data_storage import DataStorage


def main():
    storage = DataStorage()
    server = LoggingServer(1, storage)
    server.add_facade_server("http://127.0.0.1:8000/")
    server.run("127.0.0.1", 8001)


if __name__ == "__main__":
    main()
