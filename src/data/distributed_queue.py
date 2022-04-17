import hazelcast

from src.data.exceptions.hazelcast_unavailable_error import HazelcastUnavailable


class DistributedQueue:
    def __init__(self):
        try:
            self.hz = hazelcast.HazelcastClient()
            self.queue = self.hz.get_queue("messages-service-distributed-queue").blocking()
        except hazelcast.errors.IllegalStateError:
            print("Failed to connect to Hazelcast")
            self.queue = None

    def get_data(self):
        if self.queue is None:
            raise HazelcastUnavailable
        try:
            return self.queue.poll()
        except hazelcast.errors.TargetDisconnectedError as err:
            print(err)
            raise HazelcastUnavailable

    def put_data(self, msg):
        if self.queue is None:
            raise HazelcastUnavailable
        try:
            self.queue.put(msg)
        except hazelcast.errors.TargetDisconnectedError as err:
            print(err)
            raise HazelcastUnavailable

    def is_empty(self):
        if self.queue is None:
            raise HazelcastUnavailable
        try:
            return self.queue.is_empty()
        except hazelcast.errors.TargetDisconnectedError as err:
            print(err)
            raise HazelcastUnavailable
