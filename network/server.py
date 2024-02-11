import socket
import random
import time
import threading
from typing import List, Dict, Tuple, Optional

PORT = 7500
FORMAT = 'utf-8'
SERVER = '127.0.0.1'
ADDR = (SERVER, PORT)


server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
server.bind(ADDR)

def handle_client(conn, addr): # conn is socket obj, addr is info about connection. handles clients concurrently
    print(f'[NEW CONNECTION] {addr} connected.')
    connected = True
    while connected:
        msg = conn.decode(FORMAT)
        print(f'[{addr}] {msg}')

        conn.send(f'msg {msg} received'.encode(FORMAT))
def start():
    server.listen()
    print(f'[LISTENING] server is lisening on {server}')

    while True: #continuous listening
        conn, addr = server.accept() # new connection to server
        thread = threading.Thread(target=handle_client, args=(conn, addr)) # send info to handle_client
        thread.start()
        print(f'[ACTIVE CONECTIONS] {threading.activeCount() -1}')

print('[START] server is starting...')
start()