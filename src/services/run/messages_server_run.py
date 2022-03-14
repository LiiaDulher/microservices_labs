from src.services.app.messages_service import MessageServer


def main():
    server = MessageServer(2)
    server.add_facade_server("http://127.0.0.1:8000/")
    server.run("127.0.0.1", 8002)


if __name__ == "__main__":
    main()
