from src.data.data_storage import DataStorage


class LocalMap(DataStorage):
    def __init__(self):
        self.map = {}

    def save_data(self, uuid, msg):
        if uuid in self.map.keys():
            raise KeyError("Such id already exists")
        self.map[uuid] = msg

    def get_data_by_id(self, uuid):
        if uuid in self.map.keys():
            return self.map[uuid]
        raise KeyError("Such id does not exist")

    def get_all_data(self):
        all_data = ""
        for key in self.map.keys():
            all_data += self.map[key] + "\n"
        return all_data
