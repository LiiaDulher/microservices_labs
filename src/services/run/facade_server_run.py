from src.services.app.facade_service import FacadeServer


def main():
    server = FacadeServer()
    server.run("127.0.0.1", 8000)


if __name__ == "__main__":
    main()
