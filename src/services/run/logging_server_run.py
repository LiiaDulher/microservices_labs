import sys

from src.services.app.logging_service import LoggingServer


def main():
    n = len(sys.argv)
    if n == 1:
        number = 1
        facade_server = "http://127.0.0.1:8000/"
        host = "127.0.0.1"
        port = 8001
        storage_node = "http://127.0.0.1:5701/"
    elif n == 6:
        number = sys.argv[1]
        host = sys.argv[2]
        port = sys.argv[3]
        storage_node = sys.argv[4]
        facade_server = sys.argv[5]
    else:
        print("Wrong arguments number. Use default arguments or give yours in such order:\n"
              "server number, server host, server port, storage node url, facade server url")
        return
    server = LoggingServer(number, storage_node)
    server.add_facade_server(facade_server)
    server.run(host, port)


if __name__ == "__main__":
    main()
