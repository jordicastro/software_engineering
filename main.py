from splash import splashScreen
import pygame
import sys

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
def events():
    # Check for events
    for event in pygame.event.get():
        # Check for the fullscreen toggle event
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            # Toggle fullscreen mode
            pygame.display.toggle_fullscreen()
            background()
        # if user types QUIT then the screen will close 
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit() 
            sys.exit() 
    return
def background():
    #Wiping after logo
    pygame.display.set_caption('Player Selection')
    screen.fill("black")
    title()
    redX = 100
    redY = 75
    redW = X/2
    redH = Y-150
    greenX = X/2
    greenY = 75
    greenW = X/2-100
    greenH = Y-150
    # Setup player selection environment
    pygame.draw.rect(screen, red, pygame.Rect(redX, redY, redW, redH))
    pygame.draw.rect(screen, green, pygame.Rect(greenX, greenY, greenW, greenH))
    textBox("ID", red, "white", (-100+redX+redW/4), redY+30)
    textBox("ID", green, "white", (greenX+greenW/4), greenY+30)
    textBox("Name", red, "white", -100+redX+3*(redW/4), redY+30)
    textBox("Name", green, "white", greenX+3*(greenW/4), greenY+30)
    
    
    
def game():
    running = True
    splashScreen()
    screen = pygame.display.set_mode((desktop.current_w, desktop.current_h))
    background()
    while running:
        X = int(screen.get_width())
        Y = int(screen.get_height())
        pygame.display.flip()
        clock.tick(60)  # limits FPS to 60
        events()

# Run Game
game()