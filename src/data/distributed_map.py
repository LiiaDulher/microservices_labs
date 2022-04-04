import hazelcast

from data.data_storage import DataStorage


class DistributedMap(DataStorage):
    def __init__(self, storage_node):
        hz = hazelcast.HazelcastClient(cluster_members=[
                storage_node
            ])
        self.map = hz.get_map("logging-service-distributed-map").blocking()

    def save_data(self, uuid, msg):
        if self.map.contains_key(uuid):
            raise KeyError("Such id already exists")
        self.map.put(uuid, msg)

    def get_data_by_id(self, uuid):
        if self.map.contains_key(uuid):
            return self.map.get(uuid)
        raise KeyError("Such id does not exist")

    def get_all_data(self):
        values = self.map.values()
        return "\n".join(values)
