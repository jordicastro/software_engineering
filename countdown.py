# importing required library
import pygame,time, sys, os, random
from server import Server
from typing import Callable

os.environ['SDL_VIDEO_CENTERED'] = '1'

def countdown(server: Server, quit: Callable):
    # activate the pygame library .
    pygame.init()

    # create the display surface object
    # of specific dimension..e(X, Y).
    screen = pygame.display.set_mode((600,480))

    # set the pygame window name
    pygame.display.set_caption('Countdown')

    # create a surface object, image is drawn on it.
    images: pygame.image = []
    for i in range(31):
        temp = pygame.image.load("resources/countdown_images/" + str(i) + ".tif").convert()
        images.append(temp)
    background = pygame.image.load("resources/countdown_images/background.tif").convert()

    # Using blit to copy content from one surface to other
    screen.blit(background, (0, 0))
    pygame.display.update()

    clock = pygame.time.Clock()
    i = len(images) - 1 # 30
    start_time = time.time()
    while time.time() - start_time < 30:
        timerNum = images[i]
        timerNumWidth = background.get_width()/2-images[i].get_width()/2
        timerNumHeight = background.get_height()/2 - 18
        screen.blit(timerNum, (timerNumWidth, timerNumHeight))
        pygame.display.update()
        clock.tick(1)
        if(i == 17):
            # ~ Music ~
            tracks = os.listdir('resources/photon_tracks')
            # Select a random track
            track = random.choice(tracks)
            # Load and play the track
            pygame.mixer.music.load(os.path.join('resources/photon_tracks', track))
            pygame.mixer.music.play()

        i = i-1

        for event in pygame.event.get():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        quit()
                    else:
                        return

    server.start_traffic()