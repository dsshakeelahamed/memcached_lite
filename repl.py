import socket
import sys
import const


class InteractiveClient:
    def __init__(self, host, port):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("%s" % host, port))
        print("**** Client ****")
        self.client_socket = client_socket
        self.process()

    def process(self):
        while True:
            try:
                input_data = input()
                method = input_data.split()[0].lower()
                if method not in const.methods:
                    print("ERROR")
                    continue
                input_data += "\r\n"
                func = getattr(self, method)
                func(input_data)
            except Exception as e:
                sys.exit(0)
                pass

    def get(self, input_data):
        try:
            self.client_socket.send(input_data.encode('utf-8'))
            output = self.client_socket.recv(const.buffer_size)
            while True:
                if b'END' in output or b'ERROR' in output:
                    break
                output += self.client_socket.recv(const.buffer_size)
            data = output.decode('utf-8').split("\r\n")
            for value in data:
                print(value)
            return
        except:
            print("ERROR")
            pass

    def close(self):
        sys.exit(0)

    def set(self, input_data):
        try:
            byte_size = int(input_data.split()[4])
            data_to_write = ''
            while byte_size > 0:
                data = input()
                diff = data.__sizeof__() - 49
                byte_size -= diff
                if byte_size < 0:
                    print("ERROR")
                    return
                data_to_write += data
            data_to_write += "\r\n"
            self.client_socket.send(input_data.encode('utf-8'))
            self.client_socket.send(data_to_write.encode('utf-8'))
            output = self.client_socket.recv(const.buffer_size)
            while True:
                if b'STORED' in output or b'ERROR' in output:
                    break
                output += self.client_socket.recv(const.buffer_size)
            data = output.decode('utf-8').split("\r\n")
            for value in data:
                print(value)
        except:
            print("ERROR")
            pass


if __name__ == "__main__":
    InteractiveClient("127.0.0.1", 9889)
