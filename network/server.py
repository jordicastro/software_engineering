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
        data, addr = server.recvfrom(1024) #receive data from client
        msg = data.decode(FORMAT) # decode data
        print(f'[{addr}] {msg}')

        conn.sendto(f'msg {msg} received'.encode(FORMAT), addr) # send response back to client
def start():
    print(f'[LISTENING] server is listening on {server}')

    while True: #continuous listening
        data, addr = server.recvfrom(1024)
        thread = threading.Thread(target=handle_client, args=(data, addr)) # send info to handle_client
        thread.start()
        print(f'[ACTIVE CONECTIONS] {threading.activeCount() -1}')

print('[START] server is starting...')
start()