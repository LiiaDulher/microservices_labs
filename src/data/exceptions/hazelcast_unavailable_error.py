class HazelcastUnavailable(Exception):
    def __init__(self, message="Hazelcast unavailable"):
        self.message = message
        super().__init__(self.message)
