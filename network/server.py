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

class TrueServer:
    def __init__(self):
        self.server_recv = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.server_recv.bind(RECEIVE_ADDR)

        self.server_broadcast = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        
        print('[START] server is starting...')
        self.start()

    def start(self):
        print(f'[LISTENING] server is listening on {self.server_recv}')

        #while True: #continuous listening
        # initial connection from client
        print(f'[WAITING FOR CONNECTION] server is waiting for connection...')
        data, addr = self.server_recv.recvfrom(1024)
        print(f'[CONNECTION] connection from {addr} received.')
        # decode data
        equip_id = data.decode(FORMAT)
        print(f'\t[BROADCASTING] player_id {equip_id} received. broadcasting to clients...')
        self.server_broadcast.sendto(str(equip_id).encode(FORMAT), BROADCAST_ADDR) 
        
        # send info to handle_client using threads
        #thread = threading.Thread(target=self.handle_client, args=(data, addr))
        #thread.start()
        #print(f'[ACTIVE CONECTIONS] {threading.active_count() -1}')
        self.handle_client(data, addr)
        

    def handle_client(self, conn, addr): # receive dictionary (int : int) on port 7501, send back broadcast (int) on port 7500
        print(f'[NEW CONNECTION] {addr} connected.')        
        connected = True
        while connected:
            # wait receive data from client
            data, addr = self.server_recv.recvfrom(1024) 
            # decode data
            msg = data.decode(FORMAT)
            print(f'\t[RECEIVED DATA] from {addr}: {msg}')
            
            if(':' in msg):
                try:
                    transmit_id = msg.split(':')[0]
                    hit_id = msg.split(':')[1]
                except ValueError:
                    print('Invalid message format. Expected: player_id:hit_id')
                    continue
                
                print(f'\t[BROADCASTING] hit_id {hit_id}, transmit_id {transmit_id} received. broadcasting to clients...')
                self.send_hit_id(transmit_id, hit_id)
            else:
                print(f'\t[BROADCASTING] msg {msg} received and joined. broadcasting to clients...')
                self.server_broadcast.sendto(str(msg).encode(FORMAT), BROADCAST_ADDR) 
            
            
    
    def add_player(self, player_id: int) -> None:
        self.server_broadcast.sendto(str(player_id).encode(FORMAT), BROADCAST_ADDR)
        
    # transmit equipment codes after each player addition
    def send_id(self, equip_id): # sends id of newly created player & id of player hit
        # encoding id
        message = equip_id.encode(FORMAT)
        # sending msg to server
        self.server_broadcast.sendto(message, BROADCAST_ADDR)
        
    # This can be used to send the hit id to the server
    # Calls update_points to update the points of the player in the server
    # Player is only deactivated if they are hit by an enemy
    def send_hit_id(self, equip_id, hit_id):
        # Next bit assumes:
        # - 43 is Green Base
        # - 53 is Red Base
        # - Even equip_id is Green
        # - Odd equip_id is Red
        message = ''
        
        # Base got hit
        if hit_id == '43':
            if equip_id % 2 == 0:
                print(f'[GREEN BASE HIT] [FRIENDLY FIRE] {hit_id} hit by {equip_id}')
            else:
                self.update_points(equip_id, 100)
                message = f'{hit_id}'
        elif hit_id == '53':
            if equip_id % 2 != 0:  
                print(f'[RED BASE HIT] [FRIENDLY FIRE] hit by {equip_id}')
                message = f'{hit_id}'
            else:
                self.update_points(equip_id, 100)
                message = f'{hit_id}'
        
        # Player got hit
        elif (equip_id + hit_id) % 2 == 0:
            # friendly fire, both players get deactivated
            print(f'[FRIENDLY FIRE] transmitting self id')
            self.update_points(equip_id, -10)
            message = f'{equip_id}'
            print(f'\t[SENDING IDs] Sending message {message} to Server')
            self.server_broadcast.sendto(message.encode(FORMAT), BROADCAST_ADDR)
            message = f'{hit_id}'
        else:
            self.update_points(equip_id, 10)
            message = f'{hit_id}'
            
        if message != '':
            print(f'\t[SENDING IDs] Sending message {message} to Server')
            self.server_broadcast.sendto(message.encode(FORMAT), BROADCAST_ADDR)
        
    # This can be used to update the points of the player in the server
    def update_points(self, equip_id, points):
        print('Still need to implement this method')
        print('[UPDATING POINTS] updating points...')
        print(f'\t[POINTS] player {equip_id} got {points} points')
        # Must read in the information from the server about the equip_id
        # Add the points to the player's score
        # Send the updated score back to the server

    # This can bet used to wait for the start signal from the server
    # This is used for testing purposes
    #def receive_broadcast(self):  TODO: while True: for continuous broadcast listening (async?)
    #    print('in receiving method')
    #    data, addr = self.server_recv.recvfrom(1024)
    #    print(f'received data from broadcast socket : {data}')
    #    msg = data.decode(FORMAT)
    #    if msg == '202':
    #        print(f'[STARTING] game is starting')
    #        # return -> main handle start game logic (players state off -> fireable?)
            

# run server
server = TrueServer()



# manual testing from terminal
# broadcast information
#     nc -u 127.0.0.1 7501
#     1
# listen for broadcast
#     nc -ul 127.0.0.1 7500
