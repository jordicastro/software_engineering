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
    title = font.render('Edit Current Game', True, (255,255,255), (0,0,0))
    textRect = title.get_rect()
    textRect.center = (X // 2, textRect.bottom)
    return screen.blit(title, textRect)
def input_box():



    return


#Event function
def events():
    # Check for events
    for event in pygame.event.get():
        # Check for the quit event
        if event.type == pygame.QUIT:
            # Quit the game
            pygame.quit()
            sys.exit()
        # Check for keydown events
        if event.type == pygame.KEYDOWN:
            # Toggle fullscreen mode
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
            # Quit the game
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()


def game():
    running = True
    splashScreen()
    screen = pygame.display.set_mode((desktop.current_w, desktop.current_h))
    while running:
        X = int(screen.get_width())
        Y = int(screen.get_height())
        #Wiping after logo
        pygame.display.set_caption('Player Selection')
        screen.fill("black")
        title()
        # Setup player selection environment
        pygame.draw.rect(screen, red, pygame.Rect(100, 50, X/2, Y-150))
        pygame.draw.rect(screen, green, pygame.Rect((X/2), 50, X/2-100, Y-150))
        pygame.display.flip()
        clock.tick(60)  # limits FPS to 60
        events()
# Run Game
game()


