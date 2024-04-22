import pygame, sys, time
from player import Player
from server import Server
from database import Database
from textScroll import TextScroll
from typing import Callable

class ActionScreen:
    def __init__(self, screen: pygame.Surface, db: Database, server: Server, red_players: list[Player], green_players: list[Player], quit: Callable):
        self.db = db
        self.server = server
        pygame.init()
        self.screen = screen
        self.X = int(self.screen.get_width())
        self.Y = int(self.screen.get_height())
        self.red_players = red_players
        self.green_players = green_players
        self.countdown = time.time()
        self.message = TextScroll(pygame.Rect(20, self.Y//2 + 50, self.X-40, self.Y//2 - 150), pygame.font.SysFont("Liberation Sans", 30), "white", "black", [], ms_per_line=5)
        self.last_time: int = 0
        self.last_blank_time: int = 0
        self.last_update: int = 0
        self.msg_array: list[str] = []
        self.quit = quit
        self.base_hitters: list[Player] = []
        self.blanking: bool = False

    # Render text box
    def textBox(self, input, color, x, y, bg):
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(input, True, (color), (bg))
        textRect = text.get_rect()
        textRect.bottomleft = (x, y)
        return self.screen.blit(text, textRect)

    def background(self):
        # Initializing Color
        red = (128, 23, 23)
        green = (17, 122, 13)
        # Create top half sections
        top_left_rect = pygame.Rect(0, 0, self.X // 2, self.Y // 2)
        top_right_rect = pygame.Rect(self.X // 2, 0, self.X // 2, self.Y // 2)
        # Fill the screen with colors
        self.screen.fill(red, top_left_rect)
        self.screen.fill(green, top_right_rect)

    def displayScore(self):
        # Initializing Color
        red = (128, 23, 23)
        green = (17, 122, 13)

        # Fill the screen with colors
        yStart = 50
        redTotalPts = 0
        greenTotalPts = 0

        # reorder the list by highest score to lowest
        self.red_players.sort(key=lambda x: x.score, reverse=True)
        self.green_players.sort(key=lambda x: x.score, reverse=True)

        # print the player name and score for each team
        for i, player in enumerate(self.red_players):
            name = player.name
            pts = player.score
            if player in self.base_hitters:
                name = name + " HIT BASE"
            if self.blanking and (int(time.time() - self.last_blank_time) % 2) == 0 and i == 0:
                name = " "
                self.blanking = False
            elif not self.blanking and (int(time.time() - self.last_blank_time) % 2) != 0 and i == 0:
                self.blanking = True
            self.textBox(str(name), "white", 150, yStart, red)
            self.textBox(str(pts), "white", self.X/2 -100, yStart, red)
            redTotalPts = redTotalPts + pts
            yStart += 30
        yStart = 50
        for i, player in enumerate(self.green_players):
            name = player.name
            pts = player.score
            if player in self.base_hitters:
                name = name + " HIT BASE"
            if self.blanking and (int(time.time() - self.last_blank_time) % 2) == 0 and i == 0:
                name = " "
                self.blanking = False
            elif not self.blanking and (int(time.time() - self.last_blank_time) % 2) != 0 and i == 0:
                self.blanking = True
            self.textBox(name, "white", self.X//2+150, yStart, green)
            self.textBox(str(pts), "white", self.X -100, yStart, green)
            greenTotalPts = greenTotalPts + pts
            yStart += 30

        # print the total score for each team
        if redTotalPts > greenTotalPts and self.blanking:
            self.textBox(str(redTotalPts), red, self.X/2 -100, self.Y//2-16, red)
            self.textBox(str(greenTotalPts), "white", self.X -100, self.Y//2-16, green)
            if (int(time.time() - self.last_blank_time) % 2) == 0 and self.blanking:
                self.blanking = False
                self.last_blank_time = time.time()
        elif greenTotalPts > redTotalPts and self.blanking:
            self.textBox(str(redTotalPts), "white", self.X/2 -100, self.Y//2-16, red)
            self.textBox(str(greenTotalPts), green, self.X -100, self.Y//2-16, green)
            if (int(time.time() - self.last_blank_time) % 2) == 0 and self.blanking:
                self.blanking = False
                self.last_blank_time = time.time()
        else:
            self.textBox(str(redTotalPts), "white", self.X/2 -100, self.Y//2-16, red)
            self.textBox(str(greenTotalPts), "white", self.X -100, self.Y//2-16, green)
            if (int(time.time() - self.last_blank_time) % 2) != 0 and not self.blanking:
                self.blanking = True
                self.last_blank_time = time.time()

    def timerDisplay(self, currentTime, startTime):
        left = 360 - (currentTime-startTime)
        minute = int(left//60)
        second = int(left%60)
        secStr = str(second)
        if (second < 10):
            secStr = "0" + secStr
        timer = str(minute) + ":" + secStr
        self.textBox("Time Remaining " + timer, "white", 1400, 1080/2+50, "black")

    def getUpdates(self):
        # Get updates from the server (player_id, hit_id, points), once per second, and update the screen
        # who calls actionScreen.py? game file can have a function that calls this function
        # Check if there are updates from the server
        new_msg_array = []
        updateArray = self.server.points_to_game(self.last_update)
        self.last_update = self.last_update + len(updateArray)
        # parse the updateArray
        for update in updateArray:
            equip_id = update.get('equip_id')
            hit_id = update.get('hit_id')
            points = update.get('points')
            for player in self.red_players + self.green_players:
                if player.equip_id == equip_id:
                    player.score += int(points)
                    shooting_player = player
                elif player.equip_id == hit_id:
                    shot_player = player
            # conditions
            msg = ''
            if points == 10:
                # player hit another player
                msg = f'{shooting_player.name} hit {shot_player.name}'
            elif points == -10:
                # player hit friendly
                msg = f'{shooting_player.name} hit friendly {shot_player.name}'
            elif points == 100:
                # player hit opponent base
                self.base_hitters.append(shooting_player)
                msg = f'{shooting_player.name} hit '
                msg += 'Red base' if hit_id == 53 else 'Green base'
            if msg != '':
                new_msg_array.append(str(msg))
        return new_msg_array

    def render(self):
        self.background()

        if (time.time() - self.last_time) >= 1:
            for msg in self.getUpdates():
                self.message.add_line(msg)
            self.last_time = time.time()

        self.displayScore()

        # trying to update messages
        self.message.update()
        self.message.draw(self.screen)

        if ( time.time() - self.countdown >= 360):
            self.quit()

        self.timerDisplay(time.time(), self.countdown)

    def run(self):
        # Create bottom half section
        bottom_rect = pygame.Rect(0, self.Y // 2, self.X, self.Y // 2)

        # trying messages
        box = pygame.Rect(20, self.Y//2 + 50, self.X-40, self.Y//2 - 150).inflate(2, 2)
        pygame.draw.rect(self.screen, "blue", box, 1)

        self.screen.fill("black", bottom_rect)
