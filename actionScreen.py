import pygame, sys, time
from countdown import countdown

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
    for x in redTeam:
        name = x.get('name')
        textBox(screen, name, "white", 150, yStart, red)
        textBox(screen, str(0), "white", X/2 -100, yStart, red)
        redTotalPts = redTotalPts + 0
        yStart += 30
    yStart = 50
    for x in greenTeam:
        name = x.get('name')
        textBox(screen, name, "white", X//2+150, yStart, green)
        textBox(screen, str(0), "white", X -100, yStart, green)
        greenTotalPts = greenTotalPts + 0
        yStart += 30
    textBox(screen, str(redTotalPts), "white", X/2 -100, Y//2-16, red)
    textBox(screen, str(greenTotalPts), "white", X -100, Y//2-16, green)
    return
def countdownHelper():
    countdown()
def runGame(redTeam,greenTeam):
    countdownHelper()
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
        screen.fill(red, top_left_rect)
        screen.fill(green, top_right_rect)
        screen.fill((0, 0, 0), bottom_rect)
        displayScore(screen, redTeam, greenTeam)
        pygame.display.flip()
        if ( time.time() - countdown >= 6000):
            running = False
            return
        clock.tick(60)

