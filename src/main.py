from src.client.client import Client


def main():
    client_name = input("Enter client's name: ")
    client = Client(client_name)
    client.add_web_server("http://127.0.0.1:8000/")
    text = "start"
    while text.lower() != "end":
        print("Please choose one of the options or 'end' to exit")
        text = input("'Post' or 'Get': ")
        if text.lower() == "post":
            msg = input("Enter message:")
            res = client.post_message(msg)
            if res[0] != 200:
                print("Error:", res[1])
            else:
                print("Message successfully posted.")
        elif text.lower() == "get":
            res = client.get_data()
            if res[0] != 200:
                print("Error:", res[1])
            else:
                print(res[1])
                print()
        else:
            print("Please choose one of the options or 'end' to exit")
    return


if __name__ == "__main__":
    main()
