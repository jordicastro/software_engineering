import socket
import random
import time
import threading
import json
from typing import List, Dict, Tuple, Optional

RECEIVE_PORT = 7501
BROADCAST_PORT = 7500
FORMAT = 'utf-8'
SERVER = '127.0.0.1'
RECEIVE_ADDR = (SERVER, RECEIVE_PORT)
BROADCAST_ADDR = (SERVER, BROADCAST_PORT)


server_recv = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
server_recv.bind(RECEIVE_ADDR)

server_broadcast = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
server_broadcast.bind(BROADCAST_ADDR)

def handle_client(conn, addr): # receive dictionary (int : int) on port 7501, send back broadcast (int) on port 7500w
    print(f'[NEW CONNECTION] {addr} connected.')
    connected = True
    while connected:
        # wait receive data from client
        data, addr = server_recv.recvfrom(1024) 
        # decode data
        msg = data.decode(FORMAT)
        print(f'\t[RECEIVED DATA] from {addr}: {msg}')
        # extract the hit_id (second in the list)
        json_msg = json.loads(msg) # string to json
        # extract hit_id from hid_id field
        # try and catch here?
        hit_id = json_msg['hit_id']
        # send response back to client
        print(f'[SERVER] hit_id {hit_id} received. broadcasting to clients...')
        server_broadcast.sendto(hit_id.encode(FORMAT), addr) 
def start():
    print(f'[LISTENING] server is listening on {server_recv}')

    while True: #continuous listening
        # initial connection from client
        data, addr = server_recv.recvfrom(1024) # 1024 message byte size
        # msg = data.decode(FORMAT)
        # print(f'[connected]: {msg}')
        # send info to handle_client using threads
        thread = threading.Thread(target=handle_client, args=(data, addr))
        thread.start()
        print(f'[ACTIVE CONECTIONS] {threading.active_count() -1}')

print('[START] server is starting...')
start()