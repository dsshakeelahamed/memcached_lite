import os

server_address = os.getenv("SERVER_HOSTNAME","")
server_port = 9889
methods = ['set', 'get', 'close']
base_path = "/tmp"
buffer_size = 65460
MAX_VALUE = 1024 * 1024 * 10
limit = True
