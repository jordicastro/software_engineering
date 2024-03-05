from splash import splashScreen
from gui import InputBox, InputLine, Button
from database import Database
import pygame, sys, socket
from actionScreen import runGame

# Database setup
db = Database()

# pygame setup
pygame.init()
desktop = pygame.display.Info()
screen = pygame.display.set_mode((desktop.current_w-10, desktop.current_h-50))
clock = pygame.time.Clock()

#Screen coordinates
X = int(screen.get_width())
Y = int(screen.get_height())

# Initializing Color
red = (128, 23, 23)
green = (17, 122, 13)

# Bind server tx socket
SERVER_IP = '127.0.0.1'
SERVER_PORT = 7500
serverAddress = (SERVER_IP, SERVER_PORT)
sockTX = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

#title setup
def title():
    font = pygame.font.Font('freesansbold.ttf', 32)
    title = font.render('Edit Current Game', True, ("white"), ("black"))
    textRect = title.get_rect()
    textRect.center = (X // 2, textRect.bottom)
    return screen.blit(title, textRect)

def textBox(input, bg, textColor, x, y):
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(input, True, (textColor), (bg))
    textRect = text.get_rect()
    textRect.center = (x, y)
    return screen.blit(text, textRect)

#Event function
def events(input_boxes, idCheck, equipCheck, nameCheck):
    # Check for events
    for event in pygame.event.get():
        for i, box in enumerate(input_boxes):
            box.handle_event(event)

        idCheck.handle_event(event)
        equipCheck.handle_event(event)
        nameCheck.handle_event(event)

        # if user types QUIT then the screen will close
        if event.type == pygame.QUIT:
            pygame.quit()
            db.close()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                db.close()
                sys.exit()
            if event.key == pygame.K_F11:
                # Toggle fullscreen mode
                pygame.display.toggle_fullscreen()
                background()
            if event.key == pygame.K_F12:
                for box in input_boxes:
                    box.clear()
                idCheck.clear()

def background():
    #Wiping after logo
    pygame.display.set_caption('Player Selection')
    screen.fill("black")
    title()
    redX = X/2 - 100 - 400 - 100  # middle of screen, 100 left of box, 400 for width of boxes, 100 right of boxes
    redY = 75
    redW = 100+400+100            #100 left of box, 400 for width of boxes, 100 right of boxes
    redH = 720
    greenX = X/2
    greenY = 75
    greenW = 100 + 400 + 100
    greenH = 720
    # Setup player selection environment
    pygame.draw.rect(screen, red, pygame.Rect(redX, redY, redW, redH))
    pygame.draw.rect(screen, green, pygame.Rect(greenX, greenY, greenW, greenH))
    textBox("ID", red, "white", redX+100+100, redY+30)
    textBox("ID", green, "white", greenX+100+100, greenY+30)
    textBox("Name", red, "white", redX+redW-100-100, redY+30)
    textBox("Name", green, "white", greenX+greenW-100-100, greenY+30)

def inputBoxLoad(team):
    inputBoxes = []
    numberBoxes = 15
    startY = 140
    boxHeight = 32
    boxWidth = 200
    endHeight = numberBoxes * boxHeight + startY
    redBoxX = X/2-100-400
    greenBoxX = X/2+100
    if not team:
        for i in range(startY,endHeight,boxHeight): # range(starting y, ending y, increment y)
            temp = InputLine(redBoxX, i, boxWidth, boxHeight) # X, Y, W, H
            inputBoxes.append(temp)
    else:
        for i in range(startY,endHeight,boxHeight): # range(starting y, ending y, increment y)
            temp = InputLine(greenBoxX, i, boxWidth, boxHeight) # X, Y, W, H
            inputBoxes.append(temp)
    return inputBoxes

# Add data to input boxes
def inputBoxUpdate(red_boxes, green_boxes, red_players, green_players):
    # For each player in the team list, add their data to the same index in the red_boxes list
    for player in red_players:
        red_boxes[red_players.index(player)].setPlayer(player)
    for player in green_players:
        green_boxes[green_players.index(player)].setPlayer(player)

def game():
    running = True

    splashScreen()
    screen = pygame.display.set_mode((desktop.current_w, desktop.current_h))
    X = int(screen.get_width())
    Y = int(screen.get_height())
    background()
    red_boxes = inputBoxLoad(False)
    green_boxes = inputBoxLoad(True)
    # Player ID input
    idField = InputBox(X/2-100, Y/2+150, 200, 32, True)
    equipmentField = InputBox(X/2-100, Y/2+100, 200, 32, True)
    nameField = InputBox(X/2-100, Y/2+50, 200, 32, True)

    red_players = []
    green_players = []

    # Add Player function
    def addPlayer():
        # Check if ID exists
        if db.check_id(idField.getText()):
            # If ID exists, add player to interface
            print('ID exists')
            if int(equipmentField.getText()) % 2 != 0:
                red_players.append({'id': idField.getText(), 'name': db.select(idField.getText())['name']})
            else:
                green_players.append({'id': idField.getText(), 'name': db.select(idField.getText())['name']})
            # Transmit equipment code via UDP
            sockTX.sendto(equipmentField.getText().encode(), (SERVER_IP, SERVER_PORT))
            # Clear fields
            idField.clear()
            equipmentField.clear()

        else:
            # If ID does not exist, prompt for name and add to database
            print('ID does not exist')
            if addPlayerButton.getText() == 'Add Player':
                addPlayerButton.setText('Create Player')
            elif nameField.getText() != '' and idField.getText() != '':
                db.insert(idField.getText(), nameField.getText(), "NULL")
                if int(equipmentField.getText()) % 2 != 0:
                    red_players.append({'id': idField.getText(), 'name': nameField.getText()})
                else:
                    green_players.append({'id': idField.getText(), 'name': nameField.getText()})
                # Transmit equipment code via UDP
                sockTX.sendto(equipmentField.getText().encode(), (SERVER_IP, SERVER_PORT))
                # Clear fields
                addPlayerButton.setText('Add Player')
                idField.clear()
                equipmentField.clear()
                nameField.clear()


    addPlayerButton = Button(X/2-64, Y/2+200, 128, 32, addPlayer, 'Add Player')

    def onStart():
        print('Start pressed')

        #COUNTDOWN FUNCTION FIRST THEN RUN GAME
        runGame() # testing to update my branch
    # Start button
    startButton = Button(X/2-35, Y/2+250, 70, 32, onStart, 'Start')

    # Main loop
    while running:
        background()
        inputBoxUpdate(red_boxes, green_boxes, red_players, green_players)
        for box in red_boxes + green_boxes:
            box.draw(screen)
        idField.draw(screen)
        equipmentField.draw(screen)
        if addPlayerButton.getText() == 'Create Player':
            # Draw name input box
            nameField.draw(screen)
        addPlayerButton.process(screen)
        startButton.process(screen)
        pygame.display.update()
        clock.tick(60)  # limits FPS to 60
        events(red_boxes + green_boxes, idField, equipmentField, nameField)

    # Quit once loop is broken
    pygame.quit()

# Run Game
game()
