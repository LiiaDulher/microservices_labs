from src.services.app.logging_service import LoggingServer


def main():
    server = LoggingServer(1)
    server.run("127.0.0.1", 8001)


if __name__ == "__main__":
    main()
