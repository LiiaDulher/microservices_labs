import hazelcast

from src.data.data_storage import DataStorage
from src.data.exceptions.hazelcast_unavailable_error import HazelcastUnavailable


class DistributedMap(DataStorage):
    def __init__(self, storage_node):
        try:
            self.hz = hazelcast.HazelcastClient(cluster_members=[
                storage_node
            ], cluster_connect_timeout=30)
            self.map = self.hz.get_map("logging-service-distributed-map").blocking()
        except hazelcast.errors.IllegalStateError:
            print("Failed to connect to Hazelcast")
            self.map = None

    def is_unavailable(self):
        return self.map is None

    def save_data(self, uuid, msg):
        if self.is_unavailable():
            raise HazelcastUnavailable
        try:
            if self.map.contains_key(uuid):
                raise KeyError("Such id already exists")
            self.map.put(uuid, msg)
        except hazelcast.errors.TargetDisconnectedError as err:
            print(err)
            raise HazelcastUnavailable

    def get_data_by_id(self, uuid):
        if self.is_unavailable():
            raise HazelcastUnavailable
        try:
            if self.map.contains_key(uuid):
                return self.map.get(uuid)
            raise KeyError("Such id does not exist")
        except hazelcast.errors.TargetDisconnectedError as err:
            print(err)
            raise HazelcastUnavailable

    def get_all_data(self):
        if self.is_unavailable():
            raise HazelcastUnavailable
        try:
            values = self.map.values()
            return "\n".join(values) + "\n"
        except hazelcast.errors.TargetDisconnectedError as err:
            print(err)
            raise HazelcastUnavailable
