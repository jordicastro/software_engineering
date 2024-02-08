
import pygame


# pygame setup
pygame.init()
desktop = pygame.display.Info()
screen = pygame.display.set_mode((desktop.current_w, desktop.current_h))
pygame.display.set_caption('Photon')
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
def game():
    running = True
    while running:
        #Wiping after logo
        screen.fill("black")
        title()
        # Setup player selection environment
        pygame.draw.rect(screen, red, pygame.Rect(100, 50, X/2, Y-150))
        pygame.draw.rect(screen, green, pygame.Rect((X/2), 50, X/2-100, Y-150))
        

        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()



# Run Game
game()

