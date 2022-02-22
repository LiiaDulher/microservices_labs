from src.client.client import Client


def main():
    liia = Client("Liia Dulher")
    liia.add_web_server("http://127.0.0.1:8000/")
    liia.post_message("Hello")
    print(liia.get_data())
    liia.post_message("world")
    print(liia.get_data())


if __name__ == "__main__":
    main()
