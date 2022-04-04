import hazelcast


class DataStorage:
    def __init__(self, storage_node):
        # TODO: use dist_map not data
        # TODO: specify node
        # hz = hazelcast.HazelcastClient(cluster_members=[
        #         storage_node
        #     ])
        # self.dist_map = hz.get_map("logging-service-distributed-map").blocking()
        self.data = {}

    def save_data(self, uuid, msg):
        # if self.dist_map.contains_key(uuid):
        #         #     raise KeyError("Such id already exists")
        #         # self.dist_map.put(uuid, msg)
        if uuid in self.data.keys():
            raise KeyError("Such id already exists")
        self.data[uuid] = msg

    def get_data_by_id(self, uuid):
        # if self.dist_map.contains_key(uuid):
        #     return self.dist_map.get(uuid)
        if uuid in self.data.keys():
            return self.data[uuid]
        raise KeyError("Such id does not exist")

    def get_all_data(self):
        # values = self.dist_map.values()
        # return "\n".join(values)
        all_data = ""
        for key in self.data.keys():
            all_data += self.data[key] + "\n"
        return all_data
