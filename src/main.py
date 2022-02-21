from src.services.app.server import Server


def main():
    server1 = Server("my")
    server1.run("127.0.0.1", 8003)


if __name__ == "__main__":
    main()
