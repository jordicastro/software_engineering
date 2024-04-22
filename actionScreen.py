import pygame, sys, time
from countdown import countdown
from player import Player
from textScroll import TextScroll

GLOBALTEXT = "This is a really long \n test that I want to try to see \n if this works or not becuase I'm not sure if it will but yeah test \n test \n test \n test \n test \n test \n test \n test \n test \n test \n test \n test \n"
# Main game loop
def events():
    # Check for events
    for event in pygame.event.get():
        # Check for the quit event
        if event.type == pygame.QUIT:
            # Quit the game
            pygame.quit()
            sys.exit()
        # Check for the fullscreen toggle event
        if event.type == pygame.KEYDOWN:
            # Toggle fullscreen mode
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
            # Check for the quit event
            if event.key == pygame.K_ESCAPE:
                # Quit the game
                pygame.quit()
                sys.exit()

# Render text box
def textBox(screen, input, color, x, y, bg):
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(input, True, (color), (bg))
    textRect = text.get_rect()
    textRect.bottomleft = (x, y)
    return screen.blit(text, textRect)

def displayScore(screen, redTeam, greenTeam):
    # Initializing Color
    red = (128, 23, 23)
    green = (17, 122, 13)
    X = int(screen.get_width())
    Y = int(screen.get_height())

    # Fill the screen with colors
    yStart = 50
    redTotalPts = 0
    greenTotalPts = 0

    #reorder the list by highest score to lowest
    redTeam.sort(key=lambda x: x.score, reverse =True)
    greenTeam.sort(key=lambda x: x.score, reverse =True)

    #print scores
    for player in redTeam:
        name = player.name
        pts = player.score
        textBox(screen, str(name), "white", 150, yStart, red)
        textBox(screen, str(pts), "white", X/2 -100, yStart, red)
        redTotalPts = redTotalPts + pts
        yStart += 30
    yStart = 50
    for player in greenTeam:
        name = player.name
        pts = player.score
        textBox(screen, name, "white", X//2+150, yStart, green)
        textBox(screen, str(pts), "white", X -100, yStart, green)
        greenTotalPts = greenTotalPts + pts
        yStart += 30

    #print the total score for each team
    textBox(screen, str(redTotalPts), "white", X/2 -100, Y//2-16, red)
    textBox(screen, str(greenTotalPts), "white", X -100, Y//2-16, green)
    return

def timerDisplay(currentTime, startTime, screen):
    left = 360 - (currentTime-startTime)
    min = int(left//60)
    sec = int(left%60)
    secStr = str(sec)
    if (sec < 10):
        secStr = "0" + secStr
    timer = str(min) + ":" + secStr
    textBox(screen, "Time Remaining " + timer, "white", 1400, 1080/2+50, "black")
def countdownHelper(server):
    countdown(server)

def getUpdates(server, lastUpdate):

    # Get updates from the server (player_id, hit_id, points), once per second, and update the screen
    # who calls actionScreen.py? game file can have a function that calls this function
    msg_array = []
    msg = ''

    # Check if there are updates from the server
    updateArray = server.points_to_game(lastUpdate)
    lastUpdate = lastUpdate + len(updateArray)
    # parse the updateArray
    for update in updateArray:
        equip_id = update.get('equip_id')
        hit_id = update.get('hit_id')
        points = update.get('points')
        msg = f'player {equip_id}'
        # conditions
        if points == 10:
            # player hit another player
            msg = msg + ' hit player ' + hit_id
            pass
        elif points == -10:
            # player hit friendly
            msg = msg + ' hit friendly ' + hit_id
            pass
        elif points == 100:
            # player hit opponent base
            msg = msg + ' hit opponent base'
        msg_array.append(msg)

    print(msg_array)
    return msg_array
        # function pass in equip_id -> find player name

        # Update the screen 
            # callable function that takes in each update and updates the screen
def updateScreen(msg_array):
    for msg in msg_array:
        print(msg)


def runGame(redTeam,greenTeam, server):

    lastTime = 0
    lastUpdate = 0

    countdownHelper(server)
    running = True
    pygame.init()
    desktop = pygame.display.Info()
    screen = pygame.display.set_mode((1920,1080))
    clock = pygame.time.Clock()

    #Screen coordinates
    X = int(screen.get_width())
    Y = int(screen.get_height())

    # Initializing Color
    red = (128, 23, 23)
    green = (17, 122, 13)

    # Create top half sections
    top_left_rect = pygame.Rect(0, 0, X // 2, Y // 2)
    top_right_rect = pygame.Rect(X // 2, 0, X // 2, Y // 2)

    # Create bottom half section
    bottom_rect = pygame.Rect(0, Y // 2, X, Y // 2)

    
    
    # trying messages
    font = pygame.font.SysFont("Liberation Sans", 30)
    area = pygame.Rect(20, Y//2 + 50, X-40, Y//2 - 150)
    box = area.inflate(2, 2)
    pygame.draw.rect(screen, "blue", box, 1)
    
    pygame.time.delay(500)
    message = TextScroll(area, font, "white", "black", GLOBALTEXT, ms_per_line=5)
        

    screen.fill((0, 0, 0), bottom_rect)
    
    # Create text box for game events
    countdown = time.time()
    while running:
        for event in pygame.event.get():
        # Check for the quit event
            if event.type == pygame.QUIT:
                # Quit the game
                pygame.quit()
                sys.exit()
            # Check for the fullscreen toggle event
            if event.type == pygame.KEYDOWN:
                # Toggle fullscreen mode
                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
                # Check for the quit event
                if event.key == pygame.K_ESCAPE:
                    # Quit the game
                    pygame.quit()
                    sys.exit()

        if (time.time() - lastTime) >= 1000:
            msg_array = getUpdates(server, lastUpdate)
            lastTime = time.time()
            # Update the screen with the new messages
            updateScreen(msg_array)

        
        
        
        
        
        
        screen.fill(red, top_left_rect)
        screen.fill(green, top_right_rect)
        
        displayScore(screen, redTeam, greenTeam)
        
        # trying to update messages
        message.update()
        message.draw(screen)
        
        if ( time.time() - countdown >= 360):
            running = False
            return
        timerDisplay(time.time(), countdown, screen)
        pygame.display.flip()
        clock.tick(60)
