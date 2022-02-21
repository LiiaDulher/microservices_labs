class DataStorage:
    def __init__(self):
        self.data = {}

    def save_data(self, uuid, msg):
        if uuid in self.data.keys():
            raise KeyError("Such id already exists")
        self.data[uuid] = msg

    def get_data_by_id(self, uuid):
        if uuid in self.data.keys():
            return self.data[uuid]
        raise KeyError("Such id does not exist")

    def get_all_data(self):
        all_data = ""
        for key in self.data.keys():
            all_data += self.data[key] + "\n"
        return all_data
