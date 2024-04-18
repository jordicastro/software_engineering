import socket, threading
RECEIVE_PORT = 7501
BROADCAST_PORT = 7500
FORMAT = 'utf-8'
SERVER = '127.0.0.1'
RECEIVE_ADDR = (SERVER, RECEIVE_PORT)
BROADCAST_ADDR = (SERVER, BROADCAST_PORT)

class Server():
   def __init__(self):
       self.server_recv = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
       self.server_recv.bind(RECEIVE_ADDR)
       self.server_broadcast = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
       self.server_thread = threading.Thread(target=self.start)
       self.server_thread.start()

    def start(self):
        print(f'[LISTENING] server is listening on {self.server_recv}')
        
        self.up_arr = []

       # start listening for new connections
       while True:
           data, addr = self.server_recv.recvfrom(1024)
           if data:
               print(f'[CONNECTION] connection from {addr} received.')
               # decode data
               equip_id = data.decode(FORMAT)
               print(f'\t[BROADCASTING] data {equip_id} received. broadcasting to clients...')

               # send info to handle_client using threads
               client_thread = threading.Thread(target=self.handle_client(equip_id))
               client_thread.start()

   def stop(self):
       self.server_recv.close()
       self.server_broadcast.close()

    def handle_client(self, msg:str): # receive dictionary (int : int) on port 7501, send back broadcast (int) on port 7500
        if(':' in msg):
            try:
                transmit_id = msg.split(':')[0]
                hit_id = msg.split(':')[1]
            except ValueError:
                print('Invalid message format. Expected: player_id:hit_id')
                
            print(f'\t[BROADCASTING] hit_id {hit_id}, transmit_id {transmit_id} received. broadcasting to clients...')
            self.send_hit_id(transmit_id, hit_id)
        else:
            print(f'\t[BROADCASTING] msg {msg} received and joined. broadcasting to clients...')
            self.server_broadcast.sendto(str(msg).encode(FORMAT), BROADCAST_ADDR)


   def add_player(self, player_id: int) -> None:
       self.server_broadcast.sendto(str(player_id).encode(FORMAT), BROADCAST_ADDR)

   # transmit equipment codes after each player addition
   def send_id(self, equip_id): # sends id of newly created player & id of player hit
       # sending msg to server
       client_thread = threading.Thread(target=self.handle_client(str(equip_id)))
       client_thread.start()

   ## This can be used to send the hit id to the server
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
               self.update_points(equip_id, hit_id, 100)
               message = f'{hit_id}'
       elif hit_id == '53':
           if equip_id % 2 != 0:  
               print(f'[RED BASE HIT] [FRIENDLY FIRE] hit by {equip_id}')
               message = f'{hit_id}'
           else:
               self.update_points(equip_id, hit_id, 100)
               message = f'{hit_id}'
       
       # Player got hit
       elif (equip_id + hit_id) % 2 == 0:
           # friendly fire, both players get deactivated
           print(f'[FRIENDLY FIRE] transmitting self id')
           self.update_points(equip_id, hit_id, -10)
           message = f'{equip_id}'
           print(f'\t[SENDING IDs] Sending message {message} to Server')
           self.server_broadcast.sendto(message.encode(FORMAT), BROADCAST_ADDR)
           message = f'{hit_id}'
       else:
           self.update_points(equip_id, hit_id, 10)
           message = f'{hit_id}'
           
       if message != '':
           print(f'\t[SENDING IDs] Sending message {message} to Server')
           self.server_broadcast.sendto(message.encode(FORMAT), BROADCAST_ADDR)

    ## This can be used to send the hit id to the server
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
                self.update_points(equip_id, hit_id, 100)
                message = f'{hit_id}'
        elif hit_id == '53':
            if equip_id % 2 != 0:  
                print(f'[RED BASE HIT] [FRIENDLY FIRE] hit by {equip_id}')
                message = f'{hit_id}'
            else:
                self.update_points(equip_id, hit_id, 100)
                message = f'{hit_id}'
        
        # Player got hit
        elif (equip_id + hit_id) % 2 == 0:
            # friendly fire, both players get deactivated
            print(f'[FRIENDLY FIRE] transmitting self id')
            self.update_points(equip_id, hit_id, -10)
            message = f'{equip_id}'
            print(f'\t[SENDING IDs] Sending message {message} to Server')
            self.server_broadcast.sendto(message.encode(FORMAT), BROADCAST_ADDR)
            message = f'{hit_id}'
        else:
            self.update_points(equip_id, hit_id, 10)
            message = f'{hit_id}'
            
        if message != '':
            print(f'\t[SENDING IDs] Sending message {message} to Server')
            self.server_broadcast.sendto(message.encode(FORMAT), BROADCAST_ADDR)

    # This can be used to update the points of the player in the server
    def update_points(self, equip_id, hit_id, points):
        print('[UPDATING POINTS] updating points...')
        print(f'\t[POINTS] player {equip_id} got {points} points')
        
        up_dict = {"equip_id" : equip_id, "hit_id" : hit_id, "points" : points}
        self.up_arr.append(up_dict)
    
    # This is the function called by the game to read new points
    def points_to_game(self, prev_seg):
        print('[GAME CALLING FOR POINTS] sending points to game...')
        return self.up_arr[prev_seg:]