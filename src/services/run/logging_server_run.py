from src.services.app.logging_service import LoggingServer
from src.data.data_storage import DataStorage

import sys


def main():
    n = len(sys.argv)
    if n == 1:
        number = 1
        facade_server = "http://127.0.0.1:8000/"
        host = "127.0.0.1"
        port = 8001
    elif n == 5:
        number = sys.argv[1]
        host = sys.argv[2]
        port = sys.argv[3]
        facade_server = sys.argv[4]
    else:
        print("Wrong arguments number. Use default arguments or give yours in such order:\n"
              "server number, server host, server port, facade server url")
        return
    storage = DataStorage()
    server = LoggingServer(number, storage)
    server.add_facade_server(facade_server)
    server.run(host, port)


if __name__ == "__main__":
    main()
