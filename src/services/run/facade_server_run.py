from src.services.app.facade_service import FacadeServer

import sys


def main():
    n = len(sys.argv)
    if n == 1:
        host = "127.0.0.1"
        port = 8000
        logging_server = "http://127.0.0.1:8001/"
        messages_server = "http://127.0.0.1:8002/"
    elif n == 5:
        host = sys.argv[1]
        port = sys.argv[2]
        logging_server = sys.argv[3]
        messages_server = sys.argv[4]
    else:
        print("Wrong arguments number. Use default arguments or give yours in such order:\n"
              "server number, server host, server port, facade server url")
        return
    server = FacadeServer()
    server.add_logging_server(logging_server)
    server.add_messages_server(messages_server)
    server.run(host, port)


if __name__ == "__main__":
    main()
