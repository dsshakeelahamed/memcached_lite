import const
from m_client import Client

if __name__ == '__main__':
    client_list = []
    for i in range(const.load_test_connections):
        client = Client(const.server_address, 9889)
        key = "mem%s"%i
        value = "cache%s"%i
        print("Setting key:%s" % key)
        print(client.set(key,value,0, 900))
        client_list.append(client)

    for i in range(const.load_test_connections):
        key = "mem%s"%i
        client = client_list[i]
        print("getting key:%s" % key)
        print(client.get(key))