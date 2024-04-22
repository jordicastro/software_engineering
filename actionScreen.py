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
        self.last_update: int = 0
        self.msg_array: list[str] = []
        self.quit = quit

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
        for player in self.red_players:
            name = player.name
            pts = player.score
            self.textBox(str(name), "white", 150, yStart, red)
            self.textBox(str(pts), "white", self.X/2 -100, yStart, red)
            redTotalPts = redTotalPts + pts
            yStart += 30
        yStart = 50
        for player in self.green_players:
            name = player.name
            pts = player.score
            self.textBox(name, "white", self.X//2+150, yStart, green)
            self.textBox(str(pts), "white", self.X -100, yStart, green)
            greenTotalPts = greenTotalPts + pts
            yStart += 30

        # print the total score for each team
        self.textBox(str(redTotalPts), "white", self.X/2 -100, self.Y//2-16, red)
        self.textBox(str(greenTotalPts), "white", self.X -100, self.Y//2-16, green)

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
            msg = f'player {equip_id}'
            # conditions
            if points == 10:
                # player hit another player
                msg = msg + ' hit player ' + str(hit_id)
            elif points == -10:
                # player hit friendly
                msg = msg + ' hit friendly ' + str(hit_id)
            elif points == 100:
                # player hit opponent base
                msg = msg + ' hit opponent base'
            if msg != '':
                new_msg_array.append(str(msg))
        return new_msg_array

    def updateScreen(self):
        # Update the screen with the new messages
        self.message = TextScroll(pygame.Rect(20, self.Y//2 + 50, self.X-40, self.Y//2 - 150), pygame.font.SysFont("Liberation Sans", 30), "white", "black", self.msg_array, ms_per_line=5)

    def render(self):
        self.background()

        if (time.time() - self.last_time) >= 1:
            self.msg_array += self.getUpdates()
            self.last_time = time.time()
            self.updateScreen()

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

        pygame.time.delay(500)

        self.screen.fill("black", bottom_rect)
