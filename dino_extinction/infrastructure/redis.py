from redis import Redis

def instance(host, port):
    print(Redis)
    return Redis(host=host, port=port)
