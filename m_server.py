import socket
import os

import const


class Server:
    """
    A Class to emulate a low level client-server memcached model.
    """
    def __init__(self):
        """
        Initializing server side socket and binding it to server port
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((const.server_address, const.server_port))
        self.data_store = {}

    def start_server(self):
        """Start the memcached server, fork the process when a connection is established.
        :param: None
        :return: None
        """
        print("Starting Server!")
        while True:
            self.server_socket.listen()
            client_socket, addr = self.server_socket.accept()
            if client_socket:
                new_process_pid = os.fork()
                if new_process_pid == 0:
                    self.client_process(client_socket)
                else:
                    # Closing socket connection from server process
                    client_socket.close()

    def client_process(self, client):
        """ Read the input till EOF is not received.
        Call the respective method as present in the input

        :param client: Client socket
        :return: None
        """
        while client:
            try:
                input_data = client.recv(const.buffer_size)
                if not input_data:
                    self.close(client=client)
                if not input_data.endswith(b'\r\n'):
                    while True:
                        input_data += client.recv(const.buffer_size)
                        if input_data.endswith(b'\r\n'):
                            break
                input_data = input_data.strip().decode('utf-8').split()
                method = input_data[0].lower()
                if method not in const.methods:
                    client.send(("Invalid Command. Enter one of the following commands: %s\r\n" % " ".join(
                        const.methods)).encode('utf-8'))
                    continue
                # Calling respective method
                args = dict()
                args["client"] = client
                args["input_data"] = input_data
                function = getattr(Server, method)
                function(self, **args)
            except (BrokenPipeError, ConnectionResetError) as e:
                os._exit(0)
            except Exception as e:
                client.send("ERROR\r\n".encode('utf-8'))

    def set(self, **kwargs):
        """To store data in memcached server

        :param kwargs:
                client: Client socket
                input_data: a list of all set command attributes ['set', key, flag, exptime, buffer, value]
        :return: None
        """
        client = kwargs["client"]
        try:
            input_data = kwargs["input_data"]
            key = input_data[1]
            flag = int(input_data[2])
            exptime = int(input_data[3])
            buffer = int(input_data[4])
            if const.limit:
                if buffer > const.MAX_VALUE:
                    return client.send("ERROR input size limit exceeded\r\n".encode('utf-8'))
            # Checking if data is part of input or has to be read separately
            if len(input_data) != 6:
                byte_size = buffer
                final_data = ''
                while byte_size > 0:
                    data = client.recv(const.buffer_size).decode('utf-8').strip("\r\n")
                    diff = data.__sizeof__() - 49
                    byte_size -= diff
                    if byte_size < 0:
                        client.send("NOT-STORED\r\n".encode('utf-8'))
                        return client.send("CLIENT_ERROR bad data chunk\r\n".encode('utf-8'))
                    final_data += data
            else:
                final_data = input_data[5]
            file_path = os.path.join(const.base_path, "%s.txt" % key)
            with open(file_path, 'w') as file:
                file.write("%s\n" % final_data)
                file.write("%s\n" % flag)
                file.write("%s\n" % buffer)
            return client.send("STORED\r\n".encode('utf-8'))
        except IndexError as e:
            print("Insufficient args")
            raise Exception(e)
        except Exception as e:
            raise Exception(e)

    def get(self, **kwargs):
        """To retrieve data in memcached server

        :param kwargs:
                client: Client socket
                input_data: a list of all get command attributes ['get', key]
        :return: None
        """
        try:
            client = kwargs["client"]
            input_data = kwargs["input_data"]
            keys = input_data[1:]
            for key in keys:
                file_path = os.path.join(const.base_path, "%s.txt" % key)
                try:
                    with open(file_path, 'r') as file:
                        data_list = []
                        for line in file:
                            data_list.append(line.rstrip())
                        client.send("VALUE {0} {1} {2}\r\n".format(key, data_list[1], data_list[2]).encode('utf-8'))
                        client.send(("%s\r\n" % data_list[0]).encode('utf-8'))
                except FileNotFoundError as e:
                    pass
            return client.send("END\r\n".encode('utf-8'))
        except FileNotFoundError as e:
            pass
        except Exception as e:
            raise Exception(e)

    def close(self, **kwargs):
        """ To close connection from server side

        :param kwargs:
               client: Client socket
        :return: None
        """
        try:
            client = kwargs["client"]
            client.close()
            return os._exit(0)
        except Exception as e:
            raise Exception(e)






