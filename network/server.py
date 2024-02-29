import socket
# import random
# import time
import threading
# import json
from typing import List, Dict, Tuple, Optional

RECEIVE_PORT = 7501
BROADCAST_PORT = 7500
FORMAT = 'utf-8'
SERVER = '127.0.0.1'
RECEIVE_ADDR = (SERVER, RECEIVE_PORT)
BROADCAST_ADDR = (SERVER, BROADCAST_PORT)

class Server:
    def __init__(self):
        self.server_recv = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.server_recv.bind(RECEIVE_ADDR)

        self.server_broadcast = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        
        print('[START] server is starting...')
        self.start()

    def handle_client(self, conn, addr): # receive dictionary (int : int) on port 7501, send back broadcast (int) on port 7500
        print(f'[NEW CONNECTION] {addr} connected.')        
        connected = True
        while connected:
            # wait receive data from client
            data, addr = self.server_recv.recvfrom(1024) 
            # decode data
            msg = data.decode(FORMAT)
            print(f'\t[RECEIVED DATA] from {addr}: {msg}')
            try:
                transmit_id = msg.split(':')[0]
                hit_id = msg.split(':')[1]
            except ValueError:
                print('Invalid message format. Expected: player_id:hit_id')
                continue
            
            print(f'\t[BROADCASTING] hit_id {hit_id}, transmit_id {transmit_id} received. broadcasting to clients...')
            self.server_broadcast.sendto(str(hit_id).encode(FORMAT), BROADCAST_ADDR) 

    def start(self):
        print(f'[LISTENING] server is listening on {self.server_recv}')

        while True: #continuous listening
            # initial connection from client
            data, addr = self.server_recv.recvfrom(1024)
            # decode data
            equip_id = data.decode(FORMAT)
            print(f'\t[BROADCASTING] player_id {equip_id} received. broadcasting to clients...')
            self.server_broadcast.sendto(str(equip_id).encode(FORMAT), BROADCAST_ADDR) 
            
            # send info to handle_client using threads
            thread = threading.Thread(target=self.handle_client, args=(data, addr))
            thread.start()
            print(f'[ACTIVE CONECTIONS] {threading.active_count() -1}')
