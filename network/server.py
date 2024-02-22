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
        # wait receive data from client
        data, addr = server.recvfrom(1024) 
        # decode data
        msg = data.decode(FORMAT)
        print(f'\t[RECEIVED DATA] from {addr}: {msg}')
        # send response back to client
        server.sendto(f'msg {msg} received'.encode(FORMAT), addr) 
def start():
    print(f'[LISTENING] server is listening on {server}')

    while True: #continuous listening
        # initial connection from client
        data, addr = server.recvfrom(1024) # 1024 message byte size
        # msg = data.decode(FORMAT)
        # print(f'[connected]: {msg}')
        # send info to handle_client using threads
        thread = threading.Thread(target=handle_client, args=(data, addr))
        thread.start()
        print(f'[ACTIVE CONECTIONS] {threading.active_count() -1}')

print('[START] server is starting...')
start()