import sys

from services.messages_service.messages_service import MessageServer


def main():
    n = len(sys.argv)
    if n == 1:
        number = 1
        host = "127.0.0.1"
        port = 8002
    elif n == 5:
        number = sys.argv[1]
        host = sys.argv[2]
        port = sys.argv[3]
    else:
        print("Wrong arguments number. Use default arguments or give yours in such order:\n"
              "server number, server host, server port")
        return
    server = MessageServer(number, host, port)
    server.run()


if __name__ == "__main__":
    main()
