from src.client.client import Client


def main():
    liia = Client("Liia Dulher")
    liia.add_web_server("http://127.0.0.1:8000/")
    res = liia.post_message("Hello")
    if res[0] != 200:
        print(res[1])
        return
    res = liia.get_data()
    print(res[1])
    if res[0] != 200:
        return
    res = liia.post_message("world")
    if res[0] != 200:
        print(res[1])
        return
    res = liia.get_data()
    print(res[1])
    if res[0] != 200:
        return


if __name__ == "__main__":
    main()
