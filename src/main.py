from src.client.client import Client


def main():
    client_name = input("Enter client's name: ")
    client = Client(client_name)
    web_server = input("Enter web-server url: ")
    client.add_web_server(web_server)
    text = "start"
    print("Please choose one of the options or 'end' to exit\n")
    while text.lower() != "end":
        text = input("'Post' or 'Get': ")
        if text.lower() == "post":
            msg = input("Enter message: ")
            res = client.post_message(msg)
            if res[0] != 200:
                print("Error:", res[1])
            else:
                print("Message successfully posted.\n")
        elif text.lower() == "get":
            res = client.get_data()
            if res[0] != 200:
                print("Error:", res[1])
            else:
                print(res[1])
                print()
        elif text.lower() == "end":
            pass
        else:
            print("Please choose one of the options or 'end' to exit\n")
    return


if __name__ == "__main__":
    main()
