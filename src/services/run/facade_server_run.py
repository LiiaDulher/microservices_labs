import sys

from src.services.app.facade_service import FacadeServer


def main():
    n = len(sys.argv)
    if n == 1:
        host = "127.0.0.1"
        port = 8000
        logging_servers = ["http://127.0.0.1:8001/"]
        messages_server = "http://127.0.0.1:8002/"
    elif n == 5:
        host = sys.argv[1]
        port = sys.argv[2]
        logging_servers = sys.argv[3]
        logging_servers = logging_servers.split(",")
        messages_server = sys.argv[4]
    else:
        print("Wrong arguments number. Use default arguments or give yours in such order:\n"
              "server host, server port, logging servers urls(separated by coma not space), messages server url")
        return
    server = FacadeServer()
    for logging_server in logging_servers:
        server.add_logging_server(logging_server)
    server.add_messages_server(messages_server)
    server.run(host, port)


if __name__ == "__main__":
    main()
