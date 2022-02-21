from src.data.data_storage import DataStorage


def main():
    my_data = DataStorage()
    my_data.save_data(1, "msg")
    try:
        my_data.save_data(1, "Non")
    except KeyError as e:
        print(e)
    print(my_data.get_data_by_id(1))


if __name__ == "__main__":
    main()
