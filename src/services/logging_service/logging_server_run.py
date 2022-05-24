import sys

from services.logging_service.logging_service import LoggingServer


def main():
    n = len(sys.argv)
    if n == 1:
        number = 1
        host = "127.0.0.1"
        port = 8001
        storage_node = "127.0.0.1:5701"
    elif n == 5:
        number = sys.argv[1]
        host = sys.argv[2]
        port = sys.argv[3]
        storage_node = sys.argv[4]
    else:
        print("Wrong arguments number. Use default arguments or give yours in such order:\n"
              "server number, server host, server port, storage node url")
        return
    server = LoggingServer(number, host, port, storage_node)
    server.run()


if __name__ == "__main__":
    main()
