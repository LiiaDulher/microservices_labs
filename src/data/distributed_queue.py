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
        return self.queue.poll()

    def put_data(self, msg):
        if self.queue is None:
            raise HazelcastUnavailable
        self.queue.put(msg)

    def is_empty(self):
        if self.queue is None:
            raise HazelcastUnavailable
        return self.queue.is_empty()
