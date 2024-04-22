# importing required library
import pygame,time, sys, os
from typing import Callable

os.environ['SDL_VIDEO_CENTERED'] = '1'

def splashScreen(quit: Callable):
    # activate the pygame library .
    pygame.init()

    # create the display surface object
    # of specific dimension..e(X, Y).
    screen = pygame.display.set_mode((680,400))

    # set the pygame window name
    pygame.display.set_caption('Splash Image')

    # create a surface object, image is drawn on it.
    imp = pygame.image.load("resources/logo.jpg").convert()
    imp = pygame.transform.scale(imp, (screen.get_size()))

    # Using blit to copy content from one surface to other
    screen.blit(imp, (0, 0))

    # paint screen one time
    pygame.display.update()

    # loop for 5 seconds to show the splash screen
    # Also wait for possible user input
    start_time = time.time()
    while time.time() - start_time < 5:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
                else:
                    return