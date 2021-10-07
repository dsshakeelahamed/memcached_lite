import socket
import const


class Client:
    """
       A Class to connect to memcached model.
    """
    def __init__(self, host, port):
        """
            Initializing client side socket and connecting it to server
        """
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("%s" % host, port))
        self.client_socket = client_socket

    def set(self, key, value, flags, expire_time):
        """ To set the value in memcached server for given key

        :param key: key to be stored
        :param value: value to be stored
        :param flags: metadata
        :param expire_time: Time for which data is to be retained in server(not yet implemented)
        :return: True: if successfully written to server
                 False: if write failure occurs
        :exception: Error writing data to Server
        """
        try:
            size = len(value)
            if const.limit:
                if size > const.MAX_VALUE:
                    raise Exception("Input size limit exceeded")
            set_command = 'set %s %s %s %s\r\n %s\r\n' % (key, flags, expire_time, size, value)
            set_command = set_command.encode('utf-8')
            self.client_socket.send(set_command)
            response = self.client_socket.recv(const.buffer_size).strip().decode('utf-8')
            if 'NOT' in response:
                return False
            if 'STORED' in response:
                return True
            if 'ERROR' in response:
                raise Exception("Error writing data to Server")
            return False
        except Exception as e:
            raise Exception(e)

    def get(self, key):
        """To get the value from memcached server for given key

        :param key: key for which value is to be retrieved
        :return: value: The data stored in memcached server
        """
        try:
            get_command = 'get %s\r\n' % (key)
            get_command = get_command.encode('utf-8')
            self.client_socket.send(get_command)
            data = self.client_socket.recv(const.buffer_size).decode('utf-8')
            while True:
                if 'END' in data:
                    break
                if 'ERROR' in data:
                    return 'ERROR'
                data += self.client_socket.recv(const.buffer_size).decode('utf-8')
            value = data.split('\r\n')[1]
            return value.encode('utf-8')
        except Exception as e:
            raise Exception(e)

    def close(self):
        """Method to close client socket

        :return: None
        """
        try:
            self.client_socket.close()
        except Exception as e:
            pass


if __name__ == '__main__':
    c = Client('127.0.0.1', 9889)
    print(c.get("test_key"))
    print(c.set("key1", "abcd", 0, 900))
    print(c.get("key1"))
