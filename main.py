# Example file showing a basic pygame "game loop"
import pygame

# pygame setup
pygame.init()
desktop = pygame.display.Info()
screen = pygame.display.set_mode((desktop.current_w, desktop.current_h))

clock = pygame.time.Clock()
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    
 
    # Initializing Color
    color = (128, 23, 23)
    
    # Drawing Rectangle
    pygame.draw.rect(screen, color, pygame.Rect(100, 50, int(screen.get_width()/2), int(screen.get_height()-150)))

    color = (17, 122, 13)
    pygame.draw.rect(screen, color, pygame.Rect(int(screen.get_width()/2), 50, int(screen.get_width()/2)-100, int(screen.get_height()-150)))
    

    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()