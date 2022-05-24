import consul


def main():
    consul_kv = consul.Consul()
    consul_kv.kv.put('hazelcast-client-1', '127.0.0.1:5701')
    consul_kv.kv.put('hazelcast-client-2', '127.0.0.1:5702')
    consul_kv.kv.put('hazelcast-client-3', '127.0.0.1:5703')
    consul_kv.kv.put('hazelcast-map-name', 'logging-service-distributed-map')
    consul_kv.kv.put('hazelcast-queue-name', 'messages-service-distributed-queue')


if __name__ == "__main__":
    main()
