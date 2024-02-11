import socket
from typing import List, Dict, Tuple, Optional

PORT = 7501
FORMAT = 'utf-8'
SERVER = '127.0.0.1'
ADDR = (SERVER, PORT)

client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT) # to string

    client.send(message)

send('test')